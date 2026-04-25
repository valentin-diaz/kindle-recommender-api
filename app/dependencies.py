from fastapi import Request
from implicit.cpu.als import AlternatingLeastSquares as ALSModelCPU
from scipy.sparse import csr_matrix
from surprise import SVD
import typing

def get_als_model(request: Request) -> ALSModelCPU:
    if not hasattr(request.app.state, "als_model"):
        raise RuntimeError("ALS model not found in app state. Make sure to initialize it on startup.")
    return request.app.state.als_model

def get_user_item_matrix(request: Request) -> csr_matrix:
    if not hasattr(request.app.state, "user_item_matrix"):
        raise RuntimeError("User-item matrix not found in app state. Make sure to initialize it on startup.")
    return request.app.state.user_item_matrix

def get_user_id_mapping(request: Request) -> typing.Dict[str, int]:
    if not hasattr(request.app.state, "user_id_mapping"):
        raise RuntimeError("User ID mapping not found in app state. Make sure to initialize it on startup.")
    return request.app.state.user_id_mapping

def get_book_id_mapping(request: Request) -> typing.Dict[str, int]:
    if not hasattr(request.app.state, "book_id_mapping"):
        raise RuntimeError("Book ID mapping not found in app state. Make sure to initialize it on startup.")
    return request.app.state.book_id_mapping

def get_id_user_mapping(request: Request) -> typing.Dict[int, str]:
    if not hasattr(request.app.state, "id_user_mapping"):
        raise RuntimeError("ID to User mapping not found in app state. Make sure to initialize it on startup.")
    return request.app.state.id_user_mapping

def get_id_book_mapping(request: Request) -> typing.Dict[int, str]:
    if not hasattr(request.app.state, "id_book_mapping"):
        raise RuntimeError("ID to Book mapping not found in app state. Make sure to initialize it on startup.")
    return request.app.state.id_book_mapping

def get_svd_model(request: Request) -> SVD:
    if not hasattr(request.app.state, "svd_model"):
        raise RuntimeError("SVD model not found in app state. Make sure to initialize it on startup.")
    return request.app.state.svd_model