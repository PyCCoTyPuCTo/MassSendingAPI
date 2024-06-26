import csv
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from dbase.datebase import get_db
from dbase.models.users import User
from dbase.repository.bot import (
    create_new_bot,
    get_bots,
    get_bots_by_social_network,
    update_bot,
)
from schemas.bots import BotsCreate, BotsUpdate, BotsView
from routes.route_user import get_current_user


router = APIRouter(prefix="/bot", tags=["bots"])


@router.get("/", response_model=list[BotsView], status_code=status.HTTP_200_OK)
def get_bots_by_owner(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    bots = get_bots(owner_id=current_user.id, db=db)
    if not bots:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Bots for {current_user.email} not found",
        )
    return bots


@router.get(
    "/social/{social_network_id}",
    response_model=list[BotsView],
    status_code=status.HTTP_200_OK,
)
def get_bots_for_social_network(
    social_network_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    bots = get_bots_by_social_network(
        owner_id=current_user.id, social_network_id=social_network_id, db=db
    )
    if not bots:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Bots for {social_network_id} not found",
        )
    return bots


@router.post("/add-bots-files", status_code=status.HTTP_201_CREATED)
async def upload(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Download no csv file")

    contents = await file.read()
    csv_data = contents.decode("utf-8").splitlines()
    csv_reader = csv.DictReader(csv_data)
    for row in csv_reader:
        new_bot = BotsCreate(
            login=row["login"],
            password=row["password"],
            owner_id=current_user.id,
            social_network_id=row["social_network_id"],
        )
        create_new_bot(bot=new_bot, db=db)
    return {"message": "Succses"}


@router.put("/edit/{id}", response_model=BotsView)
def update_bot_info(
    bot_id: int,
    new_info_bot: BotsUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    bot = update_bot(bot_id=bot_id, bot=new_info_bot, owner_id=current_user.id, db=db)
    if not bot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Bot with id {bot_id} for user {current_user.email} does not exist",
        )
    return bot
