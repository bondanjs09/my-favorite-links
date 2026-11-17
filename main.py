from contextlib import closing
from urllib.parse import urlparse

from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from database import get_connection, init_db


app = FastAPI(title="My Favorite Links")

templates = Jinja2Templates(directory="templates")

# Initialize database
init_db()


@app.get("/", response_class=HTMLResponse)
def index(request: Request):

    with closing(get_connection()) as connection:
        contents = connection.execute("""
            SELECT id, links, created_at
            FROM content_tbl
            WHERE deleted_at IS NULL
            AND is_active = 1
            ORDER BY created_at DESC
        """).fetchall()

    return templates.TemplateResponse(
        request=request, name="index.html", context={"contents": contents}
    )


@app.post("/create")
def create_content(links: str = Form(...)):

    links = links.strip()

    parsed_url = urlparse(links)

    if parsed_url.scheme not in ["http", "https"] or not parsed_url.netloc:
        raise HTTPException(status_code=400, detail="Invalid URL")

    with closing(get_connection()) as connection:
        connection.execute(
            """
            INSERT INTO content_tbl (links)
            VALUES (?)
        """,
            (links,),
        )

        connection.commit()

    return RedirectResponse(url="/", status_code=303)


@app.post("/delete/{content_id}")
def delete_content(content_id: int):

    with closing(get_connection()) as connection:
        connection.execute(
            """
            UPDATE content_tbl
            SET is_active = 0, deleted_at = CURRENT_TIMESTAMP
            WHERE id = ?
            AND deleted_at IS NULL
        """,
            (content_id,),
        )

        connection.commit()

    return RedirectResponse(url="/", status_code=303)
