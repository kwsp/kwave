from __future__ import annotations
import types
import getpass
import platform
import typing
import importlib.metadata
from datetime import datetime
from dataclasses import dataclass, is_dataclass
from datetime import datetime
import h5py
import numpy as np


class DatasetAttrs(typing.NamedTuple):
    data_type: bytes
    domain_type: bytes


_b = np.bytes_

LongReal = typing.Annotated[np.uint64, DatasetAttrs(_b("long"), _b("real"))]
LongRealOptional = typing.Annotated[
    np.uint64 | None, DatasetAttrs(_b("long"), _b("real"))
]
FloatReal = typing.Annotated[np.float32, DatasetAttrs(_b("float"), _b("real"))]
FloatRealOptional = typing.Annotated[
    np.float32 | None, DatasetAttrs(_b("float"), _b("real"))
]


def make_input_file_attrs():
    created_by = "Python kwave " + importlib.metadata.version("kwave")
    file_description = (
        "Input data created by "
        + getpass.getuser()
        + " running "
        + platform.python_implementation()
        + " "
        + platform.python_version()
        + " on "
        + platform.machine()
        + " "
        + platform.system()
    )

    return dict(
        created_by=_b(created_by),
        creation_date=_b(datetime.now().strftime("%d-%b-%Y-%H-%M-%S")),
        file_description=_b(file_description),
        file_type=_b("input"),
        major_version=_b("1"),
        minor_version=_b("2"),
    )


def is_optional(tp, verbose=False):
    origin = typing.get_origin(tp)
    if verbose:
        print(tp, origin)
    match origin:
        case None:
            return False
        case types.UnionType | typing.Union:
            args = typing.get_args(tp)
            return any(a for a in args if a is types.NoneType)
        case typing.Annotated:
            return is_optional(typing.get_args(tp)[0], verbose=verbose)

    return False


def get_call_type(tp):
    match typing.get_origin(tp):
        case typing.Annotated:
            return get_call_type(typing.get_args(tp)[0])
        case types.UnionType | typing.Union:
            args = typing.get_args(tp)
            return get_call_type(next(a for a in args if a is not types.NoneType))
        case _:
            return tp


DClass = typing.TypeVar("DClass")


def deserialize_from_hdf5(dclass: type[DClass], f: h5py.File, verbose=False) -> DClass:
    """
    Deserialize an input HDF5 file to a dataclass.
    """
    if verbose:
        print("Parsing ", dclass)

    d = {}
    for key, anno in typing.get_type_hints(dclass).items():
        if is_dataclass(anno):
            d[key] = deserialize_from_hdf5(anno, f, verbose)
        else:
            dtype: type = get_call_type(anno)

            h5val: h5py.Dataset = f.get(key)
            if h5val is None:
                pass
            elif h5val.shape == (1, 1, 1):
                # Shape (1, 1, 1) represents a single value
                h5val = h5val[0][0][0]
                if dtype != type(h5val):
                    print(
                        f"WARNING: {key=} has type {type(h5val)}, different from annotated {dtype}."
                    )
            else:
                # Some other shape. Make a numpy array copy
                h5val = h5val[:]
                if dtype != h5val.dtype:
                    print(
                        f"WARNING: {key=} has type {type(h5val)}, different from annotated {dtype}."
                    )

            if verbose:
                print("--", key, h5val, type(h5val))

            d[key] = h5val

    return dclass(**d)


def _match_shape(s1: tuple[int, int, int], s2: tuple[int | str, int | str, int | str]):
    if len(s1) != len(s2):
        return False
    for v1, v2 in zip(s1, s2):
        assert isinstance(v1, int)
        if isinstance(v2, int) and v1 != v2:
            return False
    return True


def _check_shape_correct(
    actual_shape: tuple[int, ...], anno_shapes: tuple[tuple[int | str, ...], ...]
):
    return any(_match_shape(actual_shape, s) for s in anno_shapes)


def serialize_to_hdf5(d: object, f: h5py.File, verbose=False, _entry=True):
    """
    Serialize a dataclass to an HDF5 file.
    """
    if _entry:
        for k, v in make_input_file_attrs().items():
            f.attrs[k] = v

    for key, anno in typing.get_type_hints(d.__class__, include_extras=True).items():
        val = getattr(d, key)

        if is_dataclass(anno):
            if verbose:
                print(d.__class__)
            serialize_to_hdf5(val, f, verbose, _entry=False)
            continue

        # If value is None and annotation marked optional, skip
        if val is None:
            if is_optional(anno):
                continue
            raise ValueError(f"Missing required data '{key}' in {d.__class__}")

        # Regular data
        ## Get annotated dtype
        dtype = get_call_type(anno)
        if verbose:
            print("--", key, dtype, anno.__metadata__)

        ## Get annotated shape
        meta_attrs = anno.__metadata__[0]
        anno_shapes = ((1, 1, 1),)
        if len(anno.__metadata__) > 1:
            anno_shapes = anno.__metadata__[1:]

        ## Check type
        if isinstance(val, (int, float, np.number)):
            # single value
            val = dtype(val)
            val = np.expand_dims(val, (0, 1, 2))
        else:
            if val.dtype != dtype:
                print(
                    f"Warning: Type of {key} is {val.dtype}, but annotated {dtype}. Casting..."
                )
                val = val.astype(dtype)

        ## Check shape
        if len(val.shape) == 1:
            val = np.expand_dims(val, (0, 1))
        elif len(val.shape) == 2:
            val = np.expand_dims(val, 0)

        if not _check_shape_correct(val.shape, anno_shapes):
            raise ValueError(f"Shape mismatch {val.shape=}, {anno_shapes=}")

        dset = f.create_dataset(key, data=val)
        for attr_k, attr_v in zip(meta_attrs._fields, meta_attrs):
            dset.attrs[attr_k] = attr_v
