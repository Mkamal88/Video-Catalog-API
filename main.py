from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from schemas import VideoCreate, VideoResponse, VideoUpdate
from database import create_tables, get_db
from typing import List

from models import Video

app = FastAPI()

create_tables()


# API endpoints for CRUD operations
# Create a video
@app.post('/videos/', response_model=VideoResponse)
def create_video(video: VideoCreate, db: Session = Depends(get_db)):
    db_video = Video(title=video.title, description=video.description, duration=video.duration)
    db.add(db_video)
    db.commit()
    db.refresh(db_video)
    return VideoResponse.from_orm(db_video)


# Retrieve a video by ID
@app.get('/videos/{video_id}', response_model=VideoResponse)
def get_video(video_id: int, db: Session = Depends(get_db)):
    video = db.query(Video).filter(Video.id == video_id).first()
    if not video:
        raise HTTPException(status_code=404, detail='Video not found')
    return VideoResponse.from_orm(video)


# Update a video
@app.put('/videos/{video_id}', response_model=VideoResponse)
def update_video(video_id: int, video: VideoUpdate, db: Session = Depends(get_db)):
    db_video = db.query(Video).filter(Video.id == video_id).first()
    if not db_video:
        raise HTTPException(status_code=404, detail='Video not found')

    db_video.title = video.title
    db_video.description = video.description
    db_video.duration = video.duration
    db.commit()
    db.refresh(db_video)
    return VideoResponse.from_orm(db_video)


# Delete a video
@app.delete('/videos/{video_id}')
def delete_video(video_id: int, db: Session = Depends(get_db)):
    db_video = db.query(Video).filter(Video.id == video_id).first()
    if not db_video:
        raise HTTPException(status_code=404, detail='Video not found')

    db.delete(db_video)
    db.commit()
    return {'message': 'Video deleted'}


# Retrieve videos with pagination
@app.get('/videos/', response_model=List[VideoResponse])
def get_videos(limit: int = 10, offset: int = 0, db: Session = Depends(get_db)):
    videos = db.query(Video).offset(offset).limit(limit).all()
    return [VideoResponse.from_orm(video) for video in videos]
