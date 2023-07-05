from pydantic import BaseModel


class VideoBase(BaseModel):
    title: str
    description: str
    duration: int


class VideoCreate(VideoBase):
    pass


class VideoUpdate(VideoBase):
    pass


class VideoResponse(VideoBase):
    id: int

    class Config:
        orm_mode = True
