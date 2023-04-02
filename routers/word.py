from fastapi import APIRouter

router = APIRouter(prefix="/manage-words")


@router.get("/{user_id}")
def get_collected_words(user_id: int):
    return {"user_id": user_id, "num_of_words": 0}
