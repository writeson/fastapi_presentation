from typing import List, Tuple
from types import ModuleType

from fastapi import APIRouter, Depends
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.combined import CombinedResponseReadAll
from app.models.albums import Album, AlbumRead
from app.models.tracks import Track, TrackRead
from app.models.playlists import Playlist, PlaylistRead
from app.models.invoices import Invoice, InvoiceRead
from app.models.invoice_items import InvoiceItem, InvoiceItemRead
from app.models.playlist_track import PlaylistTrack
from app.models.customers import Customer, CustomerRead
from app.models.employees import Employee, EmployeeRead


def get_routes(
    router: APIRouter,
    model: ModuleType,
    child_models: List[ModuleType],
) -> None:
    """
    iterate through the child models and build the specific routes for each model

    :params router: the router to add the routes to
    :params model: the model to build the routes for
    :params child_models: the child models to build the routes for
    """ ""
    route_handlers = {
        "Artist": {"Album": _child_album_handler},
        "Album": {"Track": _child_track_handler},
        "Track": {
            "InvoiceItem": _child_invoice_item_handler,
            "Playlist": _child_track_playlist_handler,
        },
        "Genre": {"Track": _child_genre_track_handler},
        "MediaType": {"Track": _child_media_type_track_handler},
        "Playlist": {"Track": _child_playlist_track_handler},
        "Invoice": {"InvoiceItem": _child_invoice_invoice_item_handler},
        "Customer": {"Invoice": _child_customer_invoice_handler},
        "Employee": {
            "Customer": _child_employee_customer_handler,
            "Employee": _child_employee_employee_hander,
        },
    }
    # iterate through the child models
    for child_model in child_models:
        class_name = get_model_class_name(model)
        child_class_name = get_model_class_name(child_model)

        # create the child route
        route_handler_func = route_handlers.get(class_name, {}).get(
            child_class_name, None
        )
        if route_handler_func is not None:
            route_handler_func(router)


def _child_album_handler(router: APIRouter):
    @router.get(
        path="/{id}/albums",
        response_model=CombinedResponseReadAll[List[AlbumRead], int],
    )
    async def read_artist_albums(
        id: int,
        offset: int = 0,
        limit: int = 10,
        db: AsyncSession = Depends(get_db),
    ) -> [List[AlbumRead], int]:
        """
        Retrieve an Artist the database with a paginated
        list of associated albums
        """
        async with db as session:
            query = (
                select(Album)
                .where(Album.artist_id == id)
                .order_by(Album.id)
                .offset(offset)
                .limit(limit)
            )
            # Execute the query
            result = await session.execute(query)
            db_albums = result.scalars().all()

            # Query for total count of albums
            count_query = select(func.count(Album.id)).where(Album.artist_id == id)
            total_count = await session.scalar(count_query)

            albums = [AlbumRead.model_validate(db_album) for db_album in db_albums]

            return CombinedResponseReadAll(
                response=albums,
                total_count=total_count,
            )


def _child_track_handler(router: APIRouter):
    @router.get(
        path="/{id}/tracks",
        response_model=CombinedResponseReadAll[List[TrackRead], int],
    )
    async def read_album_tracks(
        id: int,
        offset: int = 0,
        limit: int = 10,
        db: AsyncSession = Depends(get_db),
    ) -> [List[TrackRead], int]:
        """
        Retrieve an Album the database with a paginated
        list of associated albums
        """
        async with db as session:
            query = (
                select(Track)
                .where(Track.album_id == id)
                .order_by(Track.id)
                .offset(offset)
                .limit(limit)
            )
            # Execute the query
            result = await session.execute(query)
            db_tracks = result.scalars().all()

            # Query for total count of tracks
            count_query = select(func.count(Track.id)).where(Track.album_id == id)
            total_count = await session.scalar(count_query)

            tracks = [TrackRead.model_validate(db_track) for db_track in db_tracks]

            return CombinedResponseReadAll(
                response=tracks,
                total_count=total_count,
            )


def _child_invoice_item_handler(router: APIRouter):
    @router.get(
        path="/{id}/invoice_items",
        response_model=CombinedResponseReadAll[List[InvoiceItemRead], int],
    )
    async def read_track_invoice_items(
        id: int,
        offset: int = 0,
        limit: int = 10,
        db: AsyncSession = Depends(get_db),
    ) -> [List[InvoiceItemRead], int]:
        """
        Retrieve a Track from the database with a paginated
        list of associated invoice items
        """
        async with db as session:
            query = (
                select(InvoiceItem)
                .where(InvoiceItem.track_id == id)
                .order_by(InvoiceItem.id)
                .offset(offset)
                .limit(limit)
            )
            # Execute the query
            result = await session.execute(query)
            db_invoice_items = result.scalars().all()

            # Query for total count of invoice items
            count_query = select(func.count(InvoiceItem.id)).where(
                InvoiceItem.track_id == id
            )
            total_count = await session.scalar(count_query)

            invoice_items = [
                InvoiceItemRead.model_validate(db_invoice_item)
                for db_invoice_item in db_invoice_items
            ]

            return CombinedResponseReadAll(
                response=invoice_items,
                total_count=total_count,
            )


def _child_track_playlist_handler(router: APIRouter):
    @router.get(
        path="/{id}/playlists",
        response_model=CombinedResponseReadAll[List[PlaylistRead], int],
    )
    async def read_track_playlists(
        id: int,
        offset: int = 0,
        limit: int = 10,
        db: AsyncSession = Depends(get_db),
    ) -> [List[PlaylistRead], int]:
        """
        Retrieve a Track from the database with a paginated
        list of associated playlists
        """
        async with db as session:
            query = (
                select(Playlist)
                .join(
                    PlaylistTrack, PlaylistTrack.playlist_id == Playlist.id
                )  # Join Playlist to playlist_track
                .join(
                    Track, PlaylistTrack.track_id == Track.id
                )  # Join playlist_track to Track
                .where(Track.id == id)  # Filter by the track ID
                .order_by(Playlist.id)
                .offset(offset)
                .limit(limit)
            )
            # Execute the query
            result = await session.execute(query)
            db_playlists = result.scalars().all()

            # Query for total count of playlists
            count_query = (
                select(func.count(Playlist.id))
                .join(
                    PlaylistTrack, PlaylistTrack.playlist_id == Playlist.id
                )  # Join Playlist to playlist_track
                .join(
                    Track, PlaylistTrack.track_id == Track.id
                )  # Join playlist_track to Track
                .where(Track.id == id)
            )
            total_count = await session.scalar(count_query)

            playlists = [
                PlaylistRead.model_validate(db_playlist) for db_playlist in db_playlists
            ]

            return CombinedResponseReadAll(
                response=playlists,
                total_count=total_count,
            )


def _child_genre_track_handler(router: APIRouter):
    @router.get(
        path="/{id}/tracks",
        response_model=CombinedResponseReadAll[List[TrackRead], int],
    )
    async def read_tracks(
        id: int,
        offset: int = 0,
        limit: int = 10,
        db: AsyncSession = Depends(get_db),
    ) -> [List[TrackRead], int]:
        """
        Retrieve a Genre the database with a paginated
        list of associated tracks
        """
        async with db as session:
            query = (
                select(Track)
                .where(Track.genre_id == id)
                .order_by(Track.id)
                .offset(offset)
                .limit(limit)
            )
            # Execute the query
            result = await session.execute(query)
            db_tracks = result.scalars().all()

            # Query for total count of media types
            count_query = select(func.count(Track.id)).where(Track.genre_id == id)
            total_count = await session.scalar(count_query)

            tracks = [TrackRead.model_validate(db_track) for db_track in db_tracks]

            return CombinedResponseReadAll(
                response=tracks,
                total_count=total_count,
            )


def _child_media_type_track_handler(router: APIRouter):
    @router.get(
        path="/{id}/tracks",
        response_model=CombinedResponseReadAll[List[TrackRead], int],
    )
    async def read_tracks(
        id: int,
        offset: int = 0,
        limit: int = 10,
        db: AsyncSession = Depends(get_db),
    ) -> [List[TrackRead], int]:
        """
        Retrieve a MediaType the database with a paginated
        list of associated tracks
        """
        async with db as session:
            query = (
                select(Track)
                .where(Track.media_type_id == id)
                .order_by(Track.id)
                .offset(offset)
                .limit(limit)
            )
            # Execute the query
            result = await session.execute(query)
            db_tracks = result.scalars().all()

            # Query for total count of media types
            count_query = select(func.count(Track.id)).where(Track.media_type_id == id)
            total_count = await session.scalar(count_query)

            tracks = [TrackRead.model_validate(db_track) for db_track in db_tracks]

            return CombinedResponseReadAll(
                response=tracks,
                total_count=total_count,
            )


def _child_playlist_track_handler(router: APIRouter):
    @router.get(
        path="/{id}/tracks",
        response_model=CombinedResponseReadAll[List[TrackRead], int],
    )
    async def read_playlists_track(
        id: int,
        offset: int = 0,
        limit: int = 10,
        db: AsyncSession = Depends(get_db),
    ) -> [List[TrackRead], int]:
        """
        Retrieve a Track from the database with a paginated
        list of associated playlists
        """
        async with db as session:
            query = (
                select(Track)
                .join(PlaylistTrack, PlaylistTrack.track_id == Track.id)
                .join(Playlist, PlaylistTrack.playlist_id == Playlist.id)
                .where(Playlist.id == id)
                .order_by(Track.id)
                .offset(offset)
                .limit(limit)
            )
            # Execute the query
            result = await session.execute(query)
            db_tracks = result.scalars().all()

            # Query for total count of playlists
            count_query = (
                select(func.count(Track.id))
                .join(PlaylistTrack, PlaylistTrack.track_id == Track.id)
                .join(Playlist, PlaylistTrack.playlist_id == Playlist.id)
                .where(Playlist.id == id)
            )
            total_count = await session.scalar(count_query)

            tracks = [TrackRead.model_validate(db_track) for db_track in db_tracks]

            return CombinedResponseReadAll(
                response=tracks,
                total_count=total_count,
            )


def _child_invoice_invoice_item_handler(router: APIRouter):
    @router.get(
        path="/{id}/invoice_items",
        response_model=CombinedResponseReadAll[List[InvoiceItemRead], int],
    )
    async def read_invoice_items(
        id: int,
        offset: int = 0,
        limit: int = 10,
        db: AsyncSession = Depends(get_db),
    ) -> [List[InvoiceItemRead], int]:
        """
        Retrieve a Invoice the database with a paginated
        list of associated invoice items
        """
        async with db as session:
            query = (
                select(InvoiceItem)
                .where(InvoiceItem.invoice_id == id)
                .order_by(InvoiceItem.id)
                .offset(offset)
                .limit(limit)
            )
            # Execute the query
            result = await session.execute(query)
            db_invoice_items = result.scalars().all()

            # Query for total count of invoice items
            count_query = select(func.count(InvoiceItem.id)).where(
                InvoiceItem.invoice_id == id
            )
            total_count = await session.scalar(count_query)

            invoice_items = [
                InvoiceItemRead.model_validate(db_invoice_item)
                for db_invoice_item in db_invoice_items
            ]

            return CombinedResponseReadAll(
                response=invoice_items,
                total_count=total_count,
            )


def _child_customer_invoice_handler(router: APIRouter):
    @router.get(
        path="/{id}/invoices",
        response_model=CombinedResponseReadAll[List[InvoiceRead], int],
    )
    async def read_invoices(
        id: int,
        offset: int = 0,
        limit: int = 10,
        db: AsyncSession = Depends(get_db),
    ) -> [List[InvoiceItemRead], int]:
        """
        Retrieve a Invoice the database with a paginated
        list of associated invoice items
        """
        async with db as session:
            query = (
                select(Invoice)
                .where(Invoice.customer_id == id)
                .order_by(Invoice.id)
                .offset(offset)
                .limit(limit)
            )
            # Execute the query
            result = await session.execute(query)
            db_invoices = result.scalars().all()

            # Query for total count of invoice items
            count_query = select(func.count(Invoice.id)).where(
                Invoice.customer_id == id
            )
            total_count = await session.scalar(count_query)

            invoices = [
                InvoiceRead.model_validate(db_invoice) for db_invoice in db_invoices
            ]

            return CombinedResponseReadAll(
                response=invoices,
                total_count=total_count,
            )


def _child_employee_customer_handler(router: APIRouter):
    @router.get(
        path="/{id}/customers",
        response_model=CombinedResponseReadAll[List[CustomerRead], int],
    )
    async def read_customers(
        id: int,
        offset: int = 0,
        limit: int = 10,
        db: AsyncSession = Depends(get_db),
    ) -> [List[CustomerRead], int]:
        """
        Retrieve an Employee the database with a paginated
        list of associated customers
        """
        async with db as session:
            query = (
                select(Customer)
                .where(Customer.support_rep_id == id)
                .order_by(Customer.id)
                .offset(offset)
                .limit(limit)
            )
            # Execute the query
            result = await session.execute(query)
            db_customers = result.scalars().all()

            # Query for total count of invoice items
            count_query = select(func.count(Customer.id)).where(
                Customer.support_rep_id == id
            )
            total_count = await session.scalar(count_query)

            customers = [
                CustomerRead.model_validate(db_customer) for db_customer in db_customers
            ]

            return CombinedResponseReadAll(
                response=customers,
                total_count=total_count,
            )


def _child_employee_employee_hander(router: APIRouter):
    @router.get(
        path="/{id}/reports",
        response_model=CombinedResponseReadAll[List[EmployeeRead], int],
    )
    async def read_employee_reports(
        id: int,
        offset: int = 0,
        limit: int = 10,
        db: AsyncSession = Depends(get_db),
    ) -> [List[EmployeeRead], int]:
        """
        Retrieve an Employee the database with a paginated
        list of associated employees (reports)
        """
        async with db as session:
            query = (
                select(Employee)
                .where(Employee.reports_to == id)
                .order_by(Employee.id)
                .offset(offset)
                .limit(limit)
            )
            # Execute the query
            result = await session.execute(query)
            db_employees = result.scalars().all()

            # Query for total count of invoice items
            count_query = select(func.count(Employee.id)).where(
                Employee.reports_to == id
            )
            total_count = await session.scalar(count_query)

            employees = [
                EmployeeRead.model_validate(db_employee) for db_employee in db_employees
            ]

            return CombinedResponseReadAll(
                response=employees,
                total_count=total_count,
            )


def get_model_class_name(model: ModuleType) -> Tuple[str]:
    """
    Returns the prefix, singular version of the prefix and the tags for the model

    :params model: the model module to get the names from
    :returns: Tuple[str] containing the prefix, singular version of the prefix and the class
    name for the model
    """
    model_name = model.__name__.split(".")[-1].lower()
    prefix = model_name
    prefix_singular = prefix.rstrip("s")
    class_name = prefix_singular.title().replace("_", "")
    return class_name
