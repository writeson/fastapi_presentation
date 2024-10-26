from project.app.models.artists import (
    Artist,
    ArtistBase,
    ArtistCreate,
    ArtistRead,
    ArtistUpdate,
    ArtistPatch,
)

from sqlalchemy.ext.asyncio import AsyncSession


async def create_artist(session: AsyncSession, artist: ArtistCreate):
    """
    Create a new Artist in the database from the passed in ArtistCreate model.
    Returns the created ArtistRead model.
    """
    db_artist = Artist(name=artist.name)
    session.add(db_artist)
    await session.commit()
    await session.refresh(db_artist)
    return db_artist