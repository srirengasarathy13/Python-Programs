from nicegui import ui
import psycopg
from psycopg.rows import dict_row

from datetime import date
from contextlib import contextmanager
import random
import string


# ============================================================
# CONFIGURATION
# ============================================================

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "user": "postgres",
    "password": "root",
    "dbname": "railway_booking",
}


# ============================================================
# APPLICATION STATE
# ============================================================

app_state = {
    "user_id": None,
    "user_name": None,

    "search": {
        "source": None,
        "destination": None,
        "date": None,
    },

    "train": None,

    "passengers": [],

    # Order matters:
    # First selected seat -> Passenger 1
    # Second selected seat -> Passenger 2
    # etc.
    "selected_seats": [],
}


STATIONS = [
    "Bangalore",
    "Chennai",
    "Coimbatore",
    "Hyderabad",
    "Kochi",
    "Madurai",
    "Mysore",
    "Salem",
    "Tirunelveli",
    "Trichy",
]


# ============================================================
# SAMPLE TRAINS
# ============================================================

SAMPLE_TRAINS = [
    ("12635", "Vaigai Express", "Chennai", "Madurai", "13:50", "21:20", "7h 30m", 80, 520),
    ("12636", "Vaigai Express", "Madurai", "Chennai", "06:00", "13:30", "7h 30m", 80, 520),

    ("12637", "Pandian Express", "Chennai", "Madurai", "21:40", "05:30", "7h 50m", 80, 540),
    ("12638", "Pandian Express", "Madurai", "Chennai", "21:20", "05:10", "7h 50m", 80, 540),

    ("12605", "Pallavan Express", "Chennai", "Trichy", "15:45", "20:00", "4h 15m", 70, 390),
    ("12606", "Pallavan Express", "Trichy", "Chennai", "06:00", "10:20", "4h 20m", 70, 390),

    ("12673", "Cheran Express", "Chennai", "Coimbatore", "22:15", "06:00", "7h 45m", 90, 610),
    ("12674", "Cheran Express", "Coimbatore", "Chennai", "21:00", "05:00", "8h 00m", 90, 610),

    ("20623", "Mysuru Express", "Chennai", "Mysore", "06:00", "13:00", "7h 00m", 80, 580),
    ("20624", "Mysuru Express", "Mysore", "Chennai", "14:00", "21:00", "7h 00m", 80, 580),

    ("12631", "Nellai Express", "Chennai", "Tirunelveli", "19:50", "07:00", "11h 10m", 90, 760),
    ("12632", "Nellai Express", "Tirunelveli", "Chennai", "19:45", "06:50", "11h 05m", 90, 760),

    ("12633", "Kanyakumari Express", "Chennai", "Tirunelveli", "20:10", "07:30", "11h 20m", 90, 780),

    ("12671", "Nilagiri Express", "Chennai", "Coimbatore", "21:15", "05:50", "8h 35m", 80, 650),

    ("12645", "West Coast Express", "Chennai", "Coimbatore", "13:15", "21:00", "7h 45m", 80, 590),

    ("12679", "Intercity Express", "Chennai", "Bangalore", "06:30", "13:00", "6h 30m", 70, 510),
    ("12680", "Intercity Express", "Bangalore", "Chennai", "14:00", "20:30", "6h 30m", 70, 510),

    ("12623", "Trivandrum Mail", "Chennai", "Kochi", "19:30", "08:00", "12h 30m", 90, 850),
]


# ============================================================
# DATABASE
# ============================================================

@contextmanager
def db():
    connection = psycopg.connect(
        **DB_CONFIG,
        row_factory=dict_row
    )

    try:
        yield connection
    finally:
        connection.close()


def setup_database():

    with db() as connection:

        with connection.cursor() as cursor:

            # ------------------------------------------------
            # USERS
            # ------------------------------------------------

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    email VARCHAR(150) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # ------------------------------------------------
            # TRAINS
            # ------------------------------------------------

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS trains (
                    id SERIAL PRIMARY KEY,
                    train_number VARCHAR(20) UNIQUE NOT NULL,
                    train_name VARCHAR(100) NOT NULL,
                    source VARCHAR(100) NOT NULL,
                    destination VARCHAR(100) NOT NULL,
                    departure TIME NOT NULL,
                    arrival TIME NOT NULL,
                    duration VARCHAR(30) NOT NULL,
                    seats INTEGER NOT NULL,
                    fare NUMERIC(10,2) NOT NULL
                )
            """)

            # ------------------------------------------------
            # BOOKINGS
            #
            # IMPORTANT:
            # PNR is NOT UNIQUE.
            #
            # Multiple passengers belonging to one booking
            # share the same PNR.
            # ------------------------------------------------

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS bookings (
                    id SERIAL PRIMARY KEY,
                    pnr VARCHAR(20) NOT NULL,
                    user_id INTEGER REFERENCES users(id),
                    train_id INTEGER REFERENCES trains(id),
                    journey_date DATE NOT NULL,
                    passenger_name VARCHAR(100) NOT NULL,
                    passenger_age INTEGER NOT NULL,
                    passenger_gender VARCHAR(20) NOT NULL,
                    seat_number INTEGER NOT NULL,
                    fare NUMERIC(10,2) NOT NULL,
                    status VARCHAR(30) DEFAULT 'CONFIRMED',
                    booking_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(train_id, journey_date, seat_number)
                )
            """)

            # ------------------------------------------------
            # MIGRATION
            #
            # Your previous version had:
            #
            # pnr VARCHAR(20) UNIQUE NOT NULL
            #
            # Remove that old UNIQUE constraint if it exists.
            # ------------------------------------------------

            cursor.execute("""
                DO $$
                DECLARE
                    c RECORD;
                BEGIN
                    FOR c IN
                        SELECT conname
                        FROM pg_constraint
                        WHERE conrelid = 'bookings'::regclass
                          AND contype = 'u'
                          AND array_length(conkey, 1) = 1
                          AND conkey[1] = (
                              SELECT attnum
                              FROM pg_attribute
                              WHERE attrelid = 'bookings'::regclass
                                AND attname = 'pnr'
                          )
                    LOOP
                        EXECUTE format(
                            'ALTER TABLE bookings DROP CONSTRAINT %I',
                            c.conname
                        );
                    END LOOP;
                END $$;
            """)

            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_bookings_pnr
                ON bookings(pnr)
            """)

            # ------------------------------------------------
            # INSERT SAMPLE TRAINS
            # ------------------------------------------------

            for train in SAMPLE_TRAINS:

                cursor.execute("""
                    INSERT INTO trains (
                        train_number,
                        train_name,
                        source,
                        destination,
                        departure,
                        arrival,
                        duration,
                        seats,
                        fare
                    )
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
                    ON CONFLICT (train_number) DO NOTHING
                """, train)

        connection.commit()


# ============================================================
# HELPERS
# ============================================================

def money(value):
    return f"₹{float(value):,.0f}"


def generate_pnr(connection):

    while True:

        pnr = "RG" + "".join(
            random.choices(string.digits, k=8)
        )

        with connection.cursor() as cursor:

            cursor.execute(
                "SELECT 1 FROM bookings WHERE pnr = %s LIMIT 1",
                (pnr,)
            )

            if cursor.fetchone() is None:
                return pnr


def reset_booking():

    app_state["train"] = None
    app_state["passengers"] = []
    app_state["selected_seats"] = []


def get_available_seats(train_id, journey_date):

    with db() as connection:

        with connection.cursor() as cursor:

            cursor.execute("""
                SELECT seat_number
                FROM bookings
                WHERE train_id = %s
                  AND journey_date = %s
                  AND status = 'CONFIRMED'
                ORDER BY seat_number
            """, (train_id, journey_date))

            return {
                row["seat_number"]
                for row in cursor.fetchall()
            }


def get_train_results(source, destination, journey_date):

    with db() as connection:

        with connection.cursor() as cursor:

            cursor.execute("""
                SELECT
                    t.*,
                    t.seats -
                    COALESCE(
                        (
                            SELECT COUNT(*)
                            FROM bookings b
                            WHERE b.train_id = t.id
                              AND b.journey_date = %s
                              AND b.status = 'CONFIRMED'
                        ),
                        0
                    ) AS available_seats
                FROM trains t
                WHERE t.source = %s
                  AND t.destination = %s
                ORDER BY t.departure
            """, (
                journey_date,
                source,
                destination
            ))

            return cursor.fetchall()


def get_my_bookings():

    with db() as connection:

        with connection.cursor() as cursor:

            cursor.execute("""
                SELECT
                    b.*,
                    t.train_number,
                    t.train_name,
                    t.source,
                    t.destination,
                    t.departure,
                    t.arrival,
                    t.duration
                FROM bookings b
                JOIN trains t
                    ON b.train_id = t.id
                WHERE b.user_id = %s
                ORDER BY b.booking_date DESC, b.pnr, b.id
            """, (app_state["user_id"],))

            return cursor.fetchall()


def group_bookings(rows):

    groups = {}
    result = []

    for row in rows:

        pnr = row["pnr"]

        if pnr not in groups:

            groups[pnr] = {
                "pnr": pnr,
                "rows": [],
                "train_number": row["train_number"],
                "train_name": row["train_name"],
                "source": row["source"],
                "destination": row["destination"],
                "journey_date": row["journey_date"],
                "booking_date": row["booking_date"],
            }

            result.append(groups[pnr])

        groups[pnr]["rows"].append(row)

    return result


# ============================================================
# GLOBAL CSS
# ============================================================

def add_global_css():
    ui.add_head_html("""
    <style>
        * { box-sizing: border-box; }

        html, body {
            margin: 0;
            min-height: 100%;
            background: #f5f7fb;
            font-family: Inter, ui-sans-serif, system-ui, -apple-system,
                         BlinkMacSystemFont, "Segoe UI", sans-serif;
            overflow-x: hidden;
        }

        body { color: #0f172a; }

        .rail-header {
            height: 56px;
            background: rgba(255,255,255,0.98);
            border-bottom: 1px solid #e5e7eb;
        }

        .rail-logo {
            font-size: 19px;
            font-weight: 900;
            letter-spacing: -0.5px;
        }

        .rail-logo-icon {
            width: 32px;
            height: 32px;
            border-radius: 9px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: #2563eb;
            color: white;
            font-size: 17px;
        }

        /* ---------- compact page layout ---------- */

        .rail-page {
            width: 100%;
            max-width: 1180px;
            margin: 0 auto;
            padding: 14px 18px 18px;
        }

        .home-viewport {
            min-height: calc(100vh - 56px);
            display: flex;
            align-items: flex-start;
        }

        .home-main {
            width: 100%;
            padding-top: 18px;
        }

        .hero-compact {
            background: linear-gradient(135deg, #0f172a, #1e3a8a);
            border-radius: 16px;
            color: white;
            overflow: hidden;
            min-height: 108px;
        }

        .search-card {
            border-radius: 16px;
            background: white;
            border: 1px solid #e5e7eb;
            box-shadow: 0 8px 24px rgba(15,23,42,0.06);
        }

        .search-grid {
            display: grid;
            grid-template-columns: minmax(190px, 1fr) 42px minmax(190px, 1fr)
                               minmax(180px, 0.9fr) 150px;
            align-items: end;
            gap: 10px;
            width: 100%;
        }

        .search-field { min-width: 0; }

        .train-card {
            border-radius: 14px;
            border: 1px solid #e5e7eb;
        }

        /* ---------- seat page ---------- */

        .seat-page {
            min-height: calc(100vh - 56px);
        }

        .seat-topbar {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 12px;
            margin-bottom: 10px;
        }

        .seat-layout {
            display: grid;
            grid-template-columns: minmax(0, 1fr) 280px;
            gap: 12px;
            align-items: start;
        }

        .seat-wrapper {
            background: white;
            border: 1px solid #e2e8f0;
            border-radius: 14px;
            padding: 12px;
            box-shadow: 0 8px 24px rgba(15,23,42,0.05);
        }

        .coach-header {
            background: #0f172a;
            color: white;
            border-radius: 9px;
            padding: 7px 12px;
        }

        .seat-map {
            width: 100%;
            overflow: hidden;
            padding: 2px 0 0;
        }

        .seat-sections {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 10px;
            width: 100%;
        }

        .seat-section {
            border: 1px solid #e2e8f0;
            background: #f8fafc;
            border-radius: 11px;
            padding: 7px 5px;
        }

        .seat-section-title {
            text-align: center;
            font-size: 9px;
            font-weight: 800;
            color: #94a3b8;
            letter-spacing: .08em;
            margin-bottom: 5px;
        }

        .seat-horizontal-row {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 5px;
            margin-bottom: 5px;
        }

        .seat-button {
            width: 40px !important;
            min-width: 40px !important;
            height: 34px !important;
            min-height: 34px !important;
            border-radius: 7px !important;
            font-weight: 800 !important;
            font-size: 10px !important;
            transition: all 0.12s ease !important;
            border: 1px solid #cbd5e1 !important;
            padding: 0 !important;
        }

        .seat-available {
            background: white !important;
            color: #0f172a !important;
        }

        .seat-available:hover {
            border-color: #2563eb !important;
            transform: translateY(-1px);
        }

        .seat-selected {
            background: #2563eb !important;
            color: white !important;
            border: 1px solid #1e3a8a !important;
            box-shadow: 0 0 0 2px rgba(37,99,235,0.13);
        }

        .seat-booked {
            background: #e2e8f0 !important;
            color: #94a3b8 !important;
            border-color: #cbd5e1 !important;
        }

        .seat-row-number {
            width: 20px;
            min-width: 20px;
            color: #94a3b8;
            font-size: 9px;
            font-weight: 700;
            text-align: center;
        }

        .seat-aisle {
            width: 13px;
            min-width: 13px;
        }

        .selected-summary {
            background: #eff6ff;
            border: 1px solid #bfdbfe;
            border-radius: 12px;
        }

        .seat-side-card {
            background: white;
            border: 1px solid #e2e8f0;
            border-radius: 14px;
            padding: 12px;
            box-shadow: 0 8px 24px rgba(15,23,42,0.05);
            position: sticky;
            top: 68px;
        }

        .assignment-list {
            display: grid;
            gap: 6px;
        }

        .assignment-row {
            min-height: 38px;
            padding: 7px 9px;
            border-radius: 9px;
            border: 1px solid #e2e8f0;
            background: #f8fafc;
        }

        .seat-legend {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 12px;
            font-size: 10px;
            color: #64748b;
            margin-top: 8px;
        }

        .legend-dot {
            width: 11px;
            height: 11px;
            border-radius: 4px;
            display: inline-block;
            border: 1px solid #cbd5e1;
            margin-right: 4px;
            vertical-align: -2px;
        }

        .passenger-card {
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            background: white;
        }

        @media (max-width: 950px) {
            .search-grid {
                grid-template-columns: 1fr 42px 1fr;
            }

            .search-grid .date-field { grid-column: 1 / 3; }
            .search-grid .search-action { grid-column: 3; }

            .seat-layout {
                grid-template-columns: 1fr;
            }

            .seat-side-card {
                position: static;
            }
        }

        @media (max-width: 700px) {
            .rail-page { padding: 10px 10px 14px; }

            .search-grid {
                grid-template-columns: 1fr;
                gap: 8px;
            }

            .search-grid .swap-field,
            .search-grid .date-field,
            .search-grid .search-action {
                grid-column: auto;
            }

            .search-grid .swap-field {
                justify-self: center;
                transform: rotate(90deg);
            }

            .seat-sections {
                grid-template-columns: 1fr;
            }

            .seat-button {
                width: 42px !important;
                min-width: 42px !important;
                height: 36px !important;
                min-height: 36px !important;
                font-size: 10px !important;
            }
        }
    </style>
    """)


# ============================================================
# HEADER
# ============================================================

def header():

    with ui.header().classes(
        "rail-header w-full px-4 md:px-8 items-center justify-between"
    ):

        with ui.row().classes("items-center gap-3"):

            with ui.element("div").classes("rail-logo-icon"):
                ui.icon("train")

            ui.label("RailGo").classes(
                "rail-logo text-slate-900"
            )

        with ui.row().classes("items-center gap-2"):

            if app_state["user_id"]:

                ui.button(
                    "My Bookings",
                    icon="confirmation_number",
                    on_click=lambda: ui.navigate.to("/bookings")
                ).props(
                    "flat"
                ).classes(
                    "text-slate-700"
                )

                ui.separator().props("vertical").classes(
                    "h-7 mx-1"
                )

                ui.label(
                    app_state["user_name"]
                ).classes(
                    "hidden sm:block text-sm font-semibold text-slate-600"
                )

                ui.button(
                    icon="logout",
                    on_click=logout
                ).props(
                    "flat round"
                ).tooltip(
                    "Logout"
                )


def logout():

    app_state["user_id"] = None
    app_state["user_name"] = None
    reset_booking()

    ui.navigate.to("/login")


# ============================================================
# COMMON PAGE CONTAINER
# ============================================================

def page_container():
    return ui.column().classes("rail-page gap-0")


# ============================================================
# LOGIN PAGE
# ============================================================

@ui.page("/login")
def login_page():

    add_global_css()

    with ui.column().classes(
        "w-full h-screen items-center justify-center p-4"
    ):

        with ui.card().classes(
            "w-1/3 h-14/15 p-7 rounded-3xl shadow-xl"
        ):

            with ui.row().classes(
                "items-center gap-3 mb-6"
            ):

                with ui.element("div").classes("rail-logo-icon"):
                    ui.icon("train")

                with ui.column().classes("gap-0"):
                    ui.label("RailGo").classes(
                        "text-2xl font-black text-slate-900"
                    )
                    ui.label("Railway Booking").classes(
                        "text-sm text-slate-500"
                    )

            ui.label("Welcome back").classes(
                "text-2xl font-bold text-slate-900"
            )

            ui.label(
                "Login to search trains and manage your bookings."
            ).classes(
                "text-sm text-slate-500 mb-5"
            )

            email = ui.input(
                "Email"
            ).props(
                "outlined type=email"
            ).classes(
                "w-full"
            )

            password = ui.input(
                "Password"
            ).props(
                "outlined type=password"
            ).classes(
                "w-full"
            )

            def do_login():

                if not email.value or not password.value:

                    ui.notify(
                        "Please enter email and password.",
                        type="warning"
                    )
                    return

                with db() as connection:

                    with connection.cursor() as cursor:

                        cursor.execute("""
                            SELECT id, name
                            FROM users
                            WHERE email = %s
                              AND password = %s
                        """, (
                            email.value.strip(),
                            password.value
                        ))

                        user = cursor.fetchone()

                if not user:

                    ui.notify(
                        "Invalid email or password.",
                        type="negative"
                    )
                    return

                app_state["user_id"] = user["id"]
                app_state["user_name"] = user["name"]

                ui.navigate.to("/")

            ui.button(
                "Login",
                icon="login",
                on_click=do_login
            ).props(
                "unelevated"
            ).classes(
                "w-full bg-blue-600"
            )

            ui.link(
                "Doesn't have an account? Click here","/register").props(
                "flat"
            ).classes(
                "w-full text-center"
            )


# ============================================================
# REGISTER PAGE
# ============================================================

@ui.page("/register")
def register_page():

    add_global_css()

    with ui.column().classes(
        "w-full min-h-screen items-center justify-center p-4"
    ):

        with ui.card().classes(
            "w-1/3 h-14/15 p-7 rounded-3xl shadow-xl"
        ):

            ui.label("Create your RailGo account").classes(
                "text-2xl font-black text-slate-900"
            )

            ui.label(
                "Create an account to book and manage train tickets."
            ).classes(
                "text-sm text-slate-500 mb-5"
            )

            name = ui.input(
                "Full Name"
            ).props(
                "outlined"
            ).classes(
                "w-full"
            )

            email = ui.input(
                "Email"
            ).props(
                "outlined type=email"
            ).classes(
                "w-full"
            )

            password = ui.input(
                "Password"
            ).props(
                "outlined type=password"
            ).classes(
                "w-full"
            )

            def register():

                if not name.value or not email.value or not password.value:

                    ui.notify(
                        "Please fill all fields.",
                        type="warning"
                    )
                    return

                try:

                    with db() as connection:

                        with connection.cursor() as cursor:

                            cursor.execute("""
                                INSERT INTO users (
                                    name,
                                    email,
                                    password
                                )
                                VALUES (%s,%s,%s)
                            """, (
                                name.value.strip(),
                                email.value.strip(),
                                password.value
                            ))

                        connection.commit()

                    ui.notify(
                        "Account created successfully!",
                        type="positive"
                    )

                    ui.navigate.to("/login")

                except psycopg.errors.UniqueViolation:

                    ui.notify(
                        "Email already registered.",
                        type="negative"
                    )

            ui.button(
                "Create Account",
                icon="person_add",
                on_click=register
            ).props(
                "unelevated"
            ).classes(
                "w-full h-12 bg-blue-600"
            )

            ui.link(
                "Back to Login","/login").props(
                "flat"
            ).classes(
                "w-full mt-2 text-center"
            )


# ============================================================
# HOME PAGE
# ============================================================

@ui.page("/")
def home_page():

    if not app_state["user_id"]:
        ui.navigate.to("/login")
        return

    add_global_css()
    header()

    with ui.element("div").classes("home-viewport"):
        with ui.column().classes("home-main max-w-6xl mx-auto px-4 md:px-6"):

            with ui.card().classes("hero-compact w-full px-5 py-4 mb-3"):
                with ui.row().classes("w-full items-center justify-between"):
                    with ui.column().classes("gap-0"):
                        ui.label(
                            f"Hello, {app_state['user_name']} 👋"
                        ).classes("text-sm font-semibold text-blue-100")

                        ui.label(
                            "Where are you going?"
                        ).classes("text-2xl md:text-3xl font-black")

                    ui.icon("train", size="42px").classes("text-blue-200")

            # One clean row on desktop: From | swap | To | Date | Search
            with ui.card().classes("search-card w-full max-w-2xl mx-auto p-4 md:p-5"):

            # FROM
                source = ui.select(
                    STATIONS,
                    value="Chennai",
                    label="From"
                ).props(
                    "outlined dense"
                ).classes(
                    "w-full"
                )

                # SWAP BUTTON
                with ui.row().classes("w-full justify-center -my-1"):
                    def swap():
                        old_source = source.value
                        source.value = destination.value
                        destination.value = old_source

                    ui.button(
                        icon="swap_vert",
                        on_click=swap
                    ).props(
                        "round unelevated"
                    ).classes(
                        "bg-slate-100 text-slate-700"
                    ).tooltip("Swap stations")

                # TO
                destination = ui.select(
                    STATIONS,
                    value="Madurai",
                    label="To"
                ).props(
                    "outlined dense"
                ).classes(
                    "w-full"
                )

                # DATE
                journey_date = ui.date(
                    value=str(date.today())
                ).props(
                    "outlined dense"
                ).classes(
                    "w-full"
                )

                # SEARCH
                def search_trains():
                    if source.value == destination.value:
                        ui.notify(
                            "From and To stations cannot be the same.",
                            type="warning"
                        )
                        return

                    try:
                        selected_date = date.fromisoformat(
                            str(journey_date.value)
                        )
                    except Exception:
                        ui.notify(
                            "Please select a valid journey date.",
                            type="warning"
                        )
                        return

                    if selected_date < date.today():
                        ui.notify(
                            "Journey date cannot be in the past.",
                            type="warning"
                        )
                        return

                    app_state["search"] = {
                        "source": source.value,
                        "destination": destination.value,
                        "date": str(selected_date),
                    }

                    reset_booking()
                    ui.navigate.to("/trains")

                # BUTTON AT RIGHT
                with ui.row().classes("w-full justify-end mt-2"):
                    ui.button(
                        "Search Trains",
                        icon="search",
                        on_click=search_trains
                    ).props(
                        "unelevated"
                    ).classes(
                        "bg-blue-600 px-6 h-10"
                    )


# ============================================================
# TRAIN RESULTS PAGE
# ============================================================

@ui.page("/trains")
def trains_page():

    if not app_state["user_id"]:
        ui.navigate.to("/login")
        return

    add_global_css()
    header()

    search = app_state["search"]

    with page_container():

        with ui.row().classes(
            "w-full items-center justify-between mb-5"
        ):

            with ui.column().classes("gap-0"):

                ui.label(
                    "Choose your train"
                ).classes(
                    "text-2xl font-black text-slate-900"
                )

                ui.label(
                    f"{search['source']} → {search['destination']}  •  "
                    f"{search['date']}"
                ).classes(
                    "text-sm text-slate-500"
                )

            ui.button(
                "Modify Search",
                icon="edit",
                on_click=lambda: ui.navigate.to("/")
            ).props(
                "flat"
            )

        trains = get_train_results(
            search["source"],
            search["destination"],
            search["date"]
        )

        if not trains:

            with ui.card().classes(
                "w-full p-10 items-center text-center rounded-2xl"
            ):

                ui.icon(
                    "train",
                    size="50px"
                ).classes(
                    "text-slate-300"
                )

                ui.label(
                    "No trains found"
                ).classes(
                    "text-xl font-bold text-slate-700 mt-3"
                )

                ui.label(
                    "Try another route or journey date."
                ).classes(
                    "text-sm text-slate-500"
                )

                ui.button(
                    "Search Again",
                    on_click=lambda: ui.navigate.to("/")
                ).props(
                    "unelevated"
                ).classes(
                    "mt-4 bg-blue-600"
                )

            return

        with ui.column().classes(
            "w-full gap-4"
        ):

            for train in trains:

                available = int(train["available_seats"])

                with ui.card().classes(
                    "train-card w-full p-5"
                ):

                    with ui.row().classes(
                        "w-full items-center justify-between gap-5 flex-wrap"
                    ):

                        # ------------------------------------
                        # TRAIN INFO
                        # ------------------------------------

                        with ui.column().classes(
                            "gap-0 min-w-[190px]"
                        ):

                            ui.label(
                                train["train_name"]
                            ).classes(
                                "text-lg font-bold text-slate-900"
                            )

                            ui.label(
                                train["train_number"]
                            ).classes(
                                "text-sm font-semibold text-blue-600"
                            )

                        # ------------------------------------
                        # TIMING
                        # ------------------------------------

                        with ui.row().classes(
                            "items-center gap-5"
                        ):

                            with ui.column().classes(
                                "items-center gap-0"
                            ):

                                ui.label(
                                    str(train["departure"])[:5]
                                ).classes(
                                    "text-xl font-black text-slate-900"
                                )

                                ui.label(
                                    train["source"]
                                ).classes(
                                    "text-xs text-slate-500"
                                )

                            with ui.column().classes(
                                "items-center gap-1"
                            ):

                                ui.label(
                                    train["duration"]
                                ).classes(
                                    "text-xs text-slate-400"
                                )

                                ui.icon(
                                    "arrow_forward",
                                    size="18px"
                                ).classes(
                                    "text-blue-500"
                                )

                            with ui.column().classes(
                                "items-center gap-0"
                            ):

                                ui.label(
                                    str(train["arrival"])[:5]
                                ).classes(
                                    "text-xl font-black text-slate-900"
                                )

                                ui.label(
                                    train["destination"]
                                ).classes(
                                    "text-xs text-slate-500"
                                )

                        # ------------------------------------
                        # FARE + SEATS
                        # ------------------------------------

                        with ui.column().classes(
                            "items-end gap-1 min-w-[120px]"
                        ):

                            ui.label(
                                money(train["fare"])
                            ).classes(
                                "text-xl font-black text-slate-900"
                            )

                            if available <= 5:

                                ui.label(
                                    f"Only {available} left"
                                ).classes(
                                    "text-xs font-bold text-orange-600"
                                )

                            else:

                                ui.label(
                                    f"{available} seats available"
                                ).classes(
                                    "text-xs text-green-600 font-semibold"
                                )

                        # ------------------------------------
                        # BUTTON
                        # ------------------------------------

                        def choose_train(t=train):

                            app_state["train"] = t
                            app_state["passengers"] = []
                            app_state["selected_seats"] = []

                            ui.navigate.to("/passengers")

                        button = ui.button(
                            "Select Train",
                            icon="arrow_forward",
                            on_click=choose_train
                        ).props(
                            "unelevated"
                        ).classes(
                            "bg-blue-600"
                        )

                        if available <= 0:
                            button.disable()


# ============================================================
# PASSENGER DETAILS PAGE
# ============================================================

@ui.page("/passengers")
def passenger_page():

    if not app_state["user_id"]:
        ui.navigate.to("/login")
        return

    if not app_state["train"]:
        ui.navigate.to("/trains")
        return

    add_global_css()
    header()

    train = app_state["train"]

    with page_container():

        with ui.row().classes(
            "items-center gap-3 mb-5"
        ):

            ui.button(
                icon="arrow_back",
                on_click=lambda: ui.navigate.to("/trains")
            ).props(
                "flat round"
            )

            with ui.column().classes("gap-0"):

                ui.label(
                    "Passenger Details"
                ).classes(
                    "text-2xl font-black text-slate-900"
                )

                ui.label(
                    f"{train['train_name']} • "
                    f"{train['source']} → {train['destination']}"
                ).classes(
                    "text-sm text-slate-500"
                )

        # ----------------------------------------------------
        # PASSENGER COUNT
        # ----------------------------------------------------

        with ui.card().classes(
            "w-full p-5 rounded-2xl"
        ):

            ui.label(
                "How many passengers?"
            ).classes(
                "text-lg font-bold text-slate-900"
            )

            ui.label(
                "You can book up to 6 passengers in one booking."
            ).classes(
                "text-sm text-slate-500 mb-4"
            )

            passenger_count = ui.select(
                [1, 2, 3, 4, 5, 6],
                value=1,
                label="Number of Passengers"
            ).props(
                "outlined"
            ).classes(
                "w-full max-w-xs"
            )

        passenger_container = ui.column().classes(
            "w-full gap-4 mt-5"
        )

        passenger_fields = []

        # ----------------------------------------------------
        # RENDER PASSENGER FORMS
        # ----------------------------------------------------

        def render_passenger_forms():

            passenger_container.clear()
            passenger_fields.clear()

            count = int(passenger_count.value or 1)

            with passenger_container:

                for index in range(count):

                    with ui.card().classes(
                        "passenger-card w-full p-5"
                    ):

                        with ui.row().classes(
                            "items-center gap-3 mb-4"
                        ):

                            with ui.element("div").classes(
                                "w-9 h-9 rounded-full bg-blue-100 "
                                "text-blue-700 flex items-center "
                                "justify-center font-black"
                            ):

                                ui.label(
                                    str(index + 1)
                                )

                            with ui.column().classes("gap-0"):

                                ui.label(
                                    f"Passenger {index + 1}"
                                ).classes(
                                    "font-bold text-slate-900"
                                )

                                ui.label(
                                    "Passenger information"
                                ).classes(
                                    "text-xs text-slate-400"
                                )

                        with ui.row().classes(
                            "w-full gap-3 flex-wrap"
                        ):

                            name = ui.input(
                                "Full Name"
                            ).props(
                                "outlined"
                            ).classes(
                                "flex-[2] min-w-[200px]"
                            )

                            age = ui.number(
                                "Age",
                                min=1,
                                max=120,
                                value=25
                            ).props(
                                "outlined"
                            ).classes(
                                "flex-1 min-w-[130px]"
                            )

                            gender = ui.select(
                                ["Male", "Female", "Other"],
                                value="Male",
                                label="Gender"
                            ).props(
                                "outlined"
                            ).classes(
                                "flex-1 min-w-[150px]"
                            )

                            passenger_fields.append({
                                "name": name,
                                "age": age,
                                "gender": gender,
                            })

        passenger_count.on_value_change(
            lambda e: render_passenger_forms()
        )

        render_passenger_forms()

        # ----------------------------------------------------
        # CONTINUE
        # ----------------------------------------------------

        def continue_to_seats():

            passengers = []

            for index, fields in enumerate(passenger_fields):

                name = str(fields["name"].value or "").strip()
                age = fields["age"].value
                gender = fields["gender"].value

                if not name:

                    ui.notify(
                        f"Enter the name of Passenger {index + 1}.",
                        type="warning"
                    )
                    return

                if not age:

                    ui.notify(
                        f"Enter the age of Passenger {index + 1}.",
                        type="warning"
                    )
                    return

                passengers.append({
                    "name": name,
                    "age": int(age),
                    "gender": gender,
                })

            app_state["passengers"] = passengers
            app_state["selected_seats"] = []

            ui.navigate.to("/seats")

        with ui.row().classes(
            "w-full justify-end mt-5"
        ):

            ui.button(
                "Continue to Seat Selection",
                icon="event_seat",
                on_click=continue_to_seats
            ).props(
                "unelevated"
            ).classes(
                "bg-blue-600 px-6 h-12"
            )


# ============================================================
# SEAT SELECTION PAGE
# ============================================================

@ui.page("/seats")
def seats_page():

    if not app_state["user_id"]:
        ui.navigate.to("/login")
        return

    if not app_state["train"] or not app_state["passengers"]:
        ui.navigate.to("/passengers")
        return

    add_global_css()
    header()

    train = app_state["train"]
    passengers = app_state["passengers"]

    required_seats = len(passengers)
    journey_date = app_state["search"]["date"]

    booked_seats = get_available_seats(
        train["id"],
        journey_date
    )

    selected_seats = app_state["selected_seats"]
    seat_buttons = {}

    with ui.column().classes("rail-page seat-page gap-0"):

        with ui.row().classes("seat-topbar"):
            with ui.column().classes("gap-0"):
                ui.label("Choose Seats").classes(
                    "text-xl md:text-2xl font-black text-slate-900"
                )
                ui.label(
                    f"{train['train_name']} · {train['source']} → "
                    f"{train['destination']} · {journey_date}"
                ).classes("text-xs text-slate-500")

            ui.button(
                "Back",
                icon="arrow_back",
                on_click=lambda: ui.navigate.to("/passengers")
            ).props("flat").classes("shrink-0")

        with ui.card().classes("selected-summary w-full px-3 py-2 mb-2"):
            with ui.row().classes(
                "w-full items-center justify-between gap-2 flex-wrap"
            ):
                with ui.row().classes("items-center gap-2"):
                    ui.icon("event_seat", size="22px").classes("text-blue-600")
                    with ui.column().classes("gap-0"):
                        ui.label("Seat Selection").classes(
                            "font-bold text-sm text-slate-900"
                        )
                        selection_counter = ui.label(
                            f"0 / {required_seats} selected"
                        ).classes("text-xs text-blue-700 font-semibold")

                with ui.row().classes("seat-legend"):
                    with ui.element("span"):
                        ui.element("span").classes(
                            "legend-dot bg-white"
                        )
                        ui.label("Available")
                    with ui.element("span"):
                        ui.element("span").classes(
                            "legend-dot bg-blue-600 border-blue-600"
                        )
                        ui.label("Selected")
                    with ui.element("span"):
                        ui.element("span").classes(
                            "legend-dot bg-slate-300"
                        )
                        ui.label("Booked")

        with ui.element("div").classes("seat-layout"):

            # LEFT: compact multi-column seat map
            with ui.card().classes("seat-wrapper w-full"):

                with ui.row().classes(
                    "coach-header w-full items-center justify-between mb-2"
                ):
                    ui.label("Coach A1").classes("font-bold text-sm")
                    ui.label(
                        f"{train['seats']} seats"
                    ).classes("text-xs text-slate-300")

                with ui.row().classes(
                    "w-full items-center justify-center mb-2"
                ):
                    ui.label("FRONT").classes(
                        "text-[9px] text-slate-400 font-bold tracking-widest"
                    )

                with ui.element("div").classes("seat-map"):
                    with ui.element("div").classes("seat-sections"):

                        # Split the coach into 3 compact sections.
                        section_size = 30
                        section_count = (train["seats"] + section_size - 1) // section_size

                        for section_index in range(section_count):
                            start = section_index * section_size + 1
                            end = min(
                                start + section_size - 1,
                                train["seats"]
                            )

                            with ui.element("div").classes("seat-section"):
                                ui.label(
                                    f"ROWS {((start - 1) // 4) + 1:02d}–"
                                    f"{((end - 1) // 4) + 1:02d}"
                                ).classes("seat-section-title")

                                for row_start in range(start, end + 1, 4):
                                    row_number = ((row_start - 1) // 4) + 1

                                    with ui.element("div").classes(
                                        "seat-horizontal-row"
                                    ):
                                        ui.label(
                                            f"{row_number:02d}"
                                        ).classes("seat-row-number")

                                        for offset in range(4):
                                            seat_number = row_start + offset

                                            if seat_number > end:
                                                break

                                            if offset == 2:
                                                ui.element("div").classes(
                                                    "seat-aisle"
                                                )

                                            is_booked = seat_number in booked_seats

                                            button = ui.button(
                                                str(seat_number)
                                            ).props(
                                                "unelevated"
                                            ).classes("seat-button")

                                            if is_booked:
                                                button.classes(add="seat-booked")
                                                button.disable()
                                            else:
                                                button.classes(add="seat-available")

                                                def seat_clicked(
                                                    seat=seat_number
                                                ):
                                                    if seat in selected_seats:
                                                        selected_seats.remove(seat)
                                                    else:
                                                        if len(selected_seats) >= required_seats:
                                                            ui.notify(
                                                                f"You only need {required_seats} seats.",
                                                                type="warning"
                                                            )
                                                            return

                                                        selected_seats.append(seat)

                                                    app_state["selected_seats"] = selected_seats
                                                    refresh_seat_ui()

                                                button.on("click", seat_clicked)

                                            seat_buttons[seat_number] = button

            # RIGHT: compact passenger assignment + action
            with ui.element("div").classes("seat-side-card"):

                with ui.row().classes(
                    "w-full items-center justify-between mb-2"
                ):
                    ui.label("Passengers").classes(
                        "font-bold text-sm text-slate-900"
                    )
                    ui.label(
                        f"{len(passengers)}"
                    ).classes("text-xs font-bold text-slate-500")

                assignment_container = ui.element(
                    "div"
                ).classes("assignment-list")

                def refresh_seat_ui():

                    selection_counter.set_text(
                        f"{len(selected_seats)} / {required_seats} selected"
                    )

                    for seat_number, button in seat_buttons.items():

                        if seat_number in booked_seats:
                            continue

                        button.classes(
                            remove="seat-available seat-selected"
                        )

                        if seat_number in selected_seats:
                            button.classes(add="seat-selected")
                            button.set_text(f"✓ {seat_number}")
                        else:
                            button.classes(add="seat-available")
                            button.set_text(str(seat_number))

                    assignment_container.clear()

                    with assignment_container:
                        for index, passenger in enumerate(passengers):

                            if index < len(selected_seats):
                                seat = selected_seats[index]

                                with ui.element("div").classes(
                                    "assignment-row flex items-center justify-between gap-2"
                                ):
                                    with ui.row().classes(
                                        "items-center gap-2 min-w-0"
                                    ):
                                        with ui.element("div").classes(
                                            "w-6 h-6 rounded-full bg-blue-100 "
                                            "text-blue-700 flex items-center "
                                            "justify-center font-bold text-[10px] shrink-0"
                                        ):
                                            ui.label(str(index + 1))

                                        ui.label(
                                            passenger["name"]
                                        ).classes(
                                            "text-xs font-semibold text-slate-800 truncate"
                                        )

                                    ui.chip(
                                        f"{seat}"
                                    ).props(
                                        "color=primary dense"
                                    ).classes("text-[10px]")

                            else:
                                with ui.element("div").classes(
                                    "assignment-row flex items-center justify-between gap-2"
                                ):
                                    ui.label(
                                        f"{index + 1}. {passenger['name']}"
                                    ).classes(
                                        "text-xs font-semibold text-slate-600 truncate"
                                    )
                                    ui.label(
                                        "Choose seat"
                                    ).classes(
                                        "text-[10px] text-orange-600 font-semibold shrink-0"
                                    )

                refresh_seat_ui()

                ui.separator().classes("my-2")

                def review_booking():
                    if len(selected_seats) != required_seats:
                        remaining = required_seats - len(selected_seats)
                        ui.notify(
                            f"Please select {remaining} more seat"
                            f"{'s' if remaining != 1 else ''}.",
                            type="warning"
                        )
                        return

                    ui.navigate.to("/confirm")

                ui.button(
                    "Review Booking",
                    icon="arrow_forward",
                    on_click=review_booking
                ).props("unelevated").classes(
                    "w-full bg-blue-600 h-10"
                )



# ============================================================
# CONFIRMATION PAGE
# ============================================================

@ui.page("/confirm")
def confirmation_page():

    if not app_state["user_id"]:
        ui.navigate.to("/login")
        return

    if (
        not app_state["train"]
        or not app_state["passengers"]
        or not app_state["selected_seats"]
    ):

        ui.navigate.to("/seats")
        return

    add_global_css()
    header()

    train = app_state["train"]
    passengers = app_state["passengers"]
    seats = app_state["selected_seats"]
    journey_date = app_state["search"]["date"]

    total_fare = float(train["fare"]) * len(passengers)

    with page_container():

        with ui.row().classes(
            "items-center gap-3 mb-5"
        ):

            ui.button(
                icon="arrow_back",
                on_click=lambda: ui.navigate.to("/seats")
            ).props(
                "flat round"
            )

            with ui.column().classes("gap-0"):

                ui.label(
                    "Review Your Booking"
                ).classes(
                    "text-2xl font-black text-slate-900"
                )

                ui.label(
                    "Check the details before confirming."
                ).classes(
                    "text-sm text-slate-500"
                )

        # ----------------------------------------------------
        # JOURNEY CARD
        # ----------------------------------------------------

        with ui.card().classes(
            "w-full p-5 rounded-2xl mb-4"
        ):

            ui.label(
                "Journey Details"
            ).classes(
                "text-lg font-bold text-slate-900 mb-4"
            )

            with ui.row().classes(
                "w-full items-center justify-between flex-wrap gap-5"
            ):

                with ui.column().classes("gap-0"):

                    ui.label(
                        train["train_name"]
                    ).classes(
                        "text-lg font-bold"
                    )

                    ui.label(
                        train["train_number"]
                    ).classes(
                        "text-sm text-blue-600 font-semibold"
                    )

                with ui.row().classes(
                    "items-center gap-5"
                ):

                    with ui.column().classes(
                        "items-center gap-0"
                    ):

                        ui.label(
                            str(train["departure"])[:5]
                        ).classes(
                            "text-xl font-black"
                        )

                        ui.label(
                            train["source"]
                        ).classes(
                            "text-xs text-slate-500"
                        )

                    ui.icon(
                        "arrow_forward"
                    ).classes(
                        "text-blue-500"
                    )

                    with ui.column().classes(
                        "items-center gap-0"
                    ):

                        ui.label(
                            str(train["arrival"])[:5]
                        ).classes(
                            "text-xl font-black"
                        )

                        ui.label(
                            train["destination"]
                        ).classes(
                            "text-xs text-slate-500"
                        )

                with ui.column().classes(
                    "items-end gap-0"
                ):

                    ui.label(
                        journey_date
                    ).classes(
                        "font-bold text-slate-800"
                    )

                    ui.label(
                        train["duration"]
                    ).classes(
                        "text-xs text-slate-500"
                    )

        # ----------------------------------------------------
        # PASSENGERS
        # ----------------------------------------------------

        with ui.card().classes(
            "w-full p-5 rounded-2xl mb-4"
        ):

            with ui.row().classes(
                "w-full items-center justify-between mb-4"
            ):

                ui.label(
                    f"Passengers ({len(passengers)})"
                ).classes(
                    "text-lg font-bold text-slate-900"
                )

                ui.label(
                    money(total_fare)
                ).classes(
                    "text-xl font-black text-blue-600"
                )

            for index, passenger in enumerate(passengers):

                seat = seats[index]

                with ui.row().classes(
                    "w-full items-center justify-between "
                    "p-3 rounded-xl bg-slate-50 mb-2"
                ):

                    with ui.row().classes(
                        "items-center gap-3"
                    ):

                        with ui.element("div").classes(
                            "w-8 h-8 rounded-full "
                            "bg-blue-100 text-blue-700 "
                            "flex items-center justify-center "
                            "font-bold text-sm"
                        ):

                            ui.label(
                                str(index + 1)
                            )

                        with ui.column().classes("gap-0"):

                            ui.label(
                                passenger["name"]
                            ).classes(
                                "font-semibold text-slate-800"
                            )

                            ui.label(
                                f"{passenger['age']} years • "
                                f"{passenger['gender']}"
                            ).classes(
                                "text-xs text-slate-500"
                            )

                    ui.chip(
                        f"Seat {seat}",
                        icon="event_seat"
                    ).props(
                        "color=primary"
                    )

        # ----------------------------------------------------
        # FARE
        # ----------------------------------------------------

        with ui.card().classes(
            "w-full p-5 rounded-2xl mb-5"
        ):

            with ui.row().classes(
                "w-full justify-between"
            ):

                ui.label(
                    f"{len(passengers)} × {money(train['fare'])}"
                ).classes(
                    "text-slate-600"
                )

                ui.label(
                    money(total_fare)
                ).classes(
                    "font-bold"
                )

            ui.separator().classes("my-3")

            with ui.row().classes(
                "w-full justify-between"
            ):

                ui.label(
                    "Total Fare"
                ).classes(
                    "text-lg font-bold"
                )

                ui.label(
                    money(total_fare)
                ).classes(
                    "text-2xl font-black text-blue-600"
                )

        # ----------------------------------------------------
        # CONFIRM
        # ----------------------------------------------------

        def confirm_booking():

            if len(seats) != len(passengers):

                ui.notify(
                    "Please select a seat for every passenger.",
                    type="warning"
                )
                return

            if len(set(seats)) != len(seats):

                ui.notify(
                    "Duplicate seats are not allowed.",
                    type="negative"
                )
                return

            try:

                with db() as connection:

                    with connection.cursor() as cursor:

                        # ------------------------------------
                        # Lock train row
                        # ------------------------------------

                        cursor.execute("""
                            SELECT *
                            FROM trains
                            WHERE id = %s
                            FOR UPDATE
                        """, (train["id"],))

                        locked_train = cursor.fetchone()

                        if not locked_train:

                            ui.notify(
                                "Train no longer exists.",
                                type="negative"
                            )
                            return

                        # ------------------------------------
                        # Validate seats
                        # ------------------------------------

                        for seat in seats:

                            if seat < 1 or seat > locked_train["seats"]:

                                ui.notify(
                                    f"Invalid seat number: {seat}",
                                    type="negative"
                                )
                                return

                            cursor.execute("""
                                SELECT 1
                                FROM bookings
                                WHERE train_id = %s
                                  AND journey_date = %s
                                  AND seat_number = %s
                                  AND status = 'CONFIRMED'
                                LIMIT 1
                            """, (
                                train["id"],
                                journey_date,
                                seat
                            ))

                            if cursor.fetchone():

                                connection.rollback()

                                ui.notify(
                                    f"Seat {seat} was just booked "
                                    f"by another user. Please choose again.",
                                    type="negative"
                                )

                                app_state["selected_seats"] = []

                                ui.navigate.to("/seats")
                                return

                        # ------------------------------------
                        # Generate PNR
                        # ------------------------------------

                        pnr = generate_pnr(connection)

                        # ------------------------------------
                        # Insert one row per passenger
                        # ------------------------------------

                        for passenger, seat in zip(
                            passengers,
                            seats
                        ):

                            cursor.execute("""
                                INSERT INTO bookings (
                                    pnr,
                                    user_id,
                                    train_id,
                                    journey_date,
                                    passenger_name,
                                    passenger_age,
                                    passenger_gender,
                                    seat_number,
                                    fare,
                                    status
                                )
                                VALUES (
                                    %s,%s,%s,%s,%s,
                                    %s,%s,%s,%s,'CONFIRMED'
                                )
                            """, (
                                pnr,
                                app_state["user_id"],
                                train["id"],
                                journey_date,
                                passenger["name"],
                                passenger["age"],
                                passenger["gender"],
                                seat,
                                train["fare"]
                            ))

                    connection.commit()

                app_state["selected_seats"] = []

                ui.navigate.to(
                    f"/success?pnr={pnr}"
                )

            except psycopg.errors.UniqueViolation:

                ui.notify(
                    "One of the selected seats is no longer available.",
                    type="negative"
                )

                app_state["selected_seats"] = []

                ui.navigate.to("/seats")

            except Exception as error:

                print("BOOKING ERROR:", error)

                ui.notify(
                    "Booking failed. Please try again.",
                    type="negative"
                )

        with ui.row().classes(
            "w-full justify-end"
        ):

            ui.button(
                f"Confirm & Book • {money(total_fare)}",
                icon="check_circle",
                on_click=confirm_booking
            ).props(
                "unelevated"
            ).classes(
                "bg-blue-600 h-12 px-7"
            )


# ============================================================
# SUCCESS PAGE
# ============================================================

@ui.page("/success")
def success_page():

    if not app_state["user_id"]:
        ui.navigate.to("/login")
        return

    add_global_css()
    header()

    pnr = ui.context.client.request.query_params.get("pnr")

    if not pnr:

        ui.navigate.to("/")
        return

    with db() as connection:

        with connection.cursor() as cursor:

            cursor.execute("""
                SELECT
                    b.*,
                    t.train_number,
                    t.train_name,
                    t.source,
                    t.destination,
                    t.departure,
                    t.arrival,
                    t.duration
                FROM bookings b
                JOIN trains t
                    ON b.train_id = t.id
                WHERE b.pnr = %s
                  AND b.user_id = %s
                ORDER BY b.id
            """, (
                pnr,
                app_state["user_id"]
            ))

            bookings = cursor.fetchall()

    if not bookings:

        ui.navigate.to("/")
        return

    total = sum(
        float(row["fare"])
        for row in bookings
    )

    first = bookings[0]

    with page_container():

        with ui.column().classes(
            "w-full items-center"
        ):

            with ui.card().classes(
                "success-card w-full max-w-2xl p-7 md:p-10"
            ):

                with ui.column().classes(
                    "w-full items-center text-center"
                ):

                    with ui.element("div").classes(
                        "w-16 h-16 rounded-full "
                        "bg-green-100 text-green-600 "
                        "flex items-center justify-center"
                    ):

                        ui.icon(
                            "check",
                            size="36px"
                        )

                    ui.label(
                        "Booking Confirmed!"
                    ).classes(
                        "text-3xl font-black text-slate-900 mt-4"
                    )

                    ui.label(
                        "Your railway ticket has been booked successfully."
                    ).classes(
                        "text-sm text-slate-500"
                    )

                    # ----------------------------------------
                    # PNR
                    # ----------------------------------------

                    with ui.column().classes(
                        "pnr-box w-full items-center p-5 mt-6"
                    ):

                        ui.label(
                            "PNR NUMBER"
                        ).classes(
                            "text-xs font-bold text-blue-500 tracking-widest"
                        )

                        ui.label(
                            pnr
                        ).classes(
                            "text-3xl font-black text-blue-700 tracking-wider"
                        )

                    # ----------------------------------------
                    # Journey
                    # ----------------------------------------

                    with ui.row().classes(
                        "w-full justify-between mt-6 "
                        "p-4 rounded-xl bg-slate-50"
                    ):

                        with ui.column().classes(
                            "items-start gap-0"
                        ):

                            ui.label(
                                first["train_name"]
                            ).classes(
                                "font-bold text-slate-900"
                            )

                            ui.label(
                                first["train_number"]
                            ).classes(
                                "text-xs text-blue-600"
                            )

                        with ui.column().classes(
                            "items-end gap-0"
                        ):

                            ui.label(
                                f"{first['source']} → "
                                f"{first['destination']}"
                            ).classes(
                                "font-semibold"
                            )

                            ui.label(
                                str(first["journey_date"])
                            ).classes(
                                "text-xs text-slate-500"
                            )

                    # ----------------------------------------
                    # Passengers
                    # ----------------------------------------

                    with ui.column().classes(
                        "w-full mt-5 gap-2"
                    ):

                        ui.label(
                            f"{len(bookings)} Passenger"
                            f"{'s' if len(bookings) != 1 else ''}"
                        ).classes(
                            "text-left font-bold"
                        )

                        for row in bookings:

                            with ui.row().classes(
                                "w-full items-center justify-between "
                                "p-3 rounded-xl border border-slate-200"
                            ):

                                ui.label(
                                    row["passenger_name"]
                                ).classes(
                                    "font-semibold"
                                )

                                ui.chip(
                                    f"Seat {row['seat_number']}"
                                ).props(
                                    "color=primary"
                                )

                    # ----------------------------------------
                    # Total
                    # ----------------------------------------

                    with ui.row().classes(
                        "w-full justify-between mt-5"
                    ):

                        ui.label(
                            "Total Fare"
                        ).classes(
                            "font-bold text-slate-600"
                        )

                        ui.label(
                            money(total)
                        ).classes(
                            "text-xl font-black text-blue-600"
                        )

                    # ----------------------------------------
                    # Actions
                    # ----------------------------------------

                    with ui.row().classes(
                        "w-full gap-3 mt-6"
                    ):

                        ui.button(
                            "My Bookings",
                            icon="confirmation_number",
                            on_click=lambda: ui.navigate.to("/bookings")
                        ).props(
                            "unelevated"
                        ).classes(
                            "flex-1 bg-blue-600 h-12"
                        )

                        ui.button(
                            "Book Another",
                            icon="add",
                            on_click=lambda: ui.navigate.to("/")
                        ).props(
                            "outline"
                        ).classes(
                            "flex-1 h-12"
                        )


# ============================================================
# MY BOOKINGS PAGE
# ============================================================

@ui.page("/bookings")
def bookings_page():

    if not app_state["user_id"]:
        ui.navigate.to("/login")
        return

    add_global_css()
    header()

    with page_container():

        with ui.row().classes(
            "w-full items-center justify-between mb-5"
        ):

            with ui.column().classes("gap-0"):

                ui.label(
                    "My Bookings"
                ).classes(
                    "text-2xl font-black text-slate-900"
                )

                ui.label(
                    "View and manage your railway bookings."
                ).classes(
                    "text-sm text-slate-500"
                )

            ui.button(
                "Book a Journey",
                icon="add",
                on_click=lambda: ui.navigate.to("/")
            ).props(
                "unelevated"
            ).classes(
                "bg-blue-600"
            )

        rows = get_my_bookings()

        if not rows:

            with ui.card().classes(
                "w-full p-10 rounded-2xl items-center text-center"
            ):

                ui.icon(
                    "confirmation_number",
                    size="50px"
                ).classes(
                    "text-slate-300"
                )

                ui.label(
                    "No bookings yet"
                ).classes(
                    "text-xl font-bold text-slate-700 mt-3"
                )

                ui.label(
                    "Your booked journeys will appear here."
                ).classes(
                    "text-sm text-slate-500"
                )

                ui.button(
                    "Search Trains",
                    icon="search",
                    on_click=lambda: ui.navigate.to("/")
                ).props(
                    "unelevated"
                ).classes(
                    "mt-4 bg-blue-600"
                )

            return

        groups = group_bookings(rows)

        with ui.column().classes(
            "w-full gap-4"
        ):

            for group in groups:

                booking_rows = group["rows"]

                statuses = {
                    row["status"]
                    for row in booking_rows
                }

                is_cancelled = statuses == {"CANCELLED"}

                total = sum(
                    float(row["fare"])
                    for row in booking_rows
                    if row["status"] != "CANCELLED"
                )

                with ui.card().classes(
                    "w-full p-5 rounded-2xl"
                ):

                    # ----------------------------------------
                    # Booking header
                    # ----------------------------------------

                    with ui.row().classes(
                        "w-full items-center justify-between "
                        "flex-wrap gap-3"
                    ):

                        with ui.column().classes("gap-0"):

                            ui.label(
                                group["train_name"]
                            ).classes(
                                "text-lg font-bold text-slate-900"
                            )

                            ui.label(
                                group["train_number"]
                            ).classes(
                                "text-sm text-blue-600 font-semibold"
                            )

                        with ui.column().classes(
                            "items-end gap-1"
                        ):

                            ui.label(
                                f"PNR: {group['pnr']}"
                            ).classes(
                                "font-bold text-slate-800"
                            )

                            if is_cancelled:

                                ui.chip(
                                    "CANCELLED",
                                    icon="cancel"
                                ).props(
                                    "color=negative"
                                )

                            else:

                                ui.chip(
                                    "CONFIRMED",
                                    icon="check_circle"
                                ).props(
                                    "color=positive"
                                )

                    ui.separator().classes("my-4")

                    # ----------------------------------------
                    # Route
                    # ----------------------------------------

                    with ui.row().classes(
                        "w-full items-center gap-4 flex-wrap"
                    ):

                        with ui.column().classes("gap-0"):

                            ui.label(
                                group["source"]
                            ).classes(
                                "text-lg font-bold"
                            )

                            ui.label(
                                "From"
                            ).classes(
                                "text-xs text-slate-400"
                            )

                        ui.icon(
                            "arrow_forward"
                        ).classes(
                            "text-blue-500"
                        )

                        with ui.column().classes("gap-0"):

                            ui.label(
                                group["destination"]
                            ).classes(
                                "text-lg font-bold"
                            )

                            ui.label(
                                "To"
                            ).classes(
                                "text-xs text-slate-400"
                            )

                        ui.separator().props(
                            "vertical"
                        ).classes(
                            "h-10 mx-2"
                        )

                        with ui.column().classes("gap-0"):

                            ui.label(
                                str(group["journey_date"])
                            ).classes(
                                "font-bold"
                            )

                            ui.label(
                                "Journey Date"
                            ).classes(
                                "text-xs text-slate-400"
                            )

                    # ----------------------------------------
                    # Passengers
                    # ----------------------------------------

                    with ui.column().classes(
                        "w-full mt-4 gap-2"
                    ):

                        ui.label(
                            f"{len(booking_rows)} passenger"
                            f"{'s' if len(booking_rows) != 1 else ''}"
                        ).classes(
                            "font-bold text-slate-700"
                        )

                        for row in booking_rows:

                            with ui.row().classes(
                                "w-full items-center "
                                "justify-between "
                                "p-3 rounded-xl bg-slate-50"
                            ):

                                with ui.column().classes("gap-0"):

                                    ui.label(
                                        row["passenger_name"]
                                    ).classes(
                                        "font-semibold text-slate-800"
                                    )

                                    ui.label(
                                        f"{row['passenger_age']} years • "
                                        f"{row['passenger_gender']}"
                                    ).classes(
                                        "text-xs text-slate-500"
                                    )

                                ui.chip(
                                    f"Seat {row['seat_number']}"
                                ).props(
                                    "color=primary"
                                )

                    # ----------------------------------------
                    # Footer
                    # ----------------------------------------

                    with ui.row().classes(
                        "w-full items-center justify-between mt-4"
                    ):

                        if is_cancelled:

                            ui.label(
                                "This booking has been cancelled."
                            ).classes(
                                "text-sm text-red-500"
                            )

                        else:

                            ui.label(
                                f"Total: {money(total)}"
                            ).classes(
                                "text-lg font-black text-slate-900"
                            )

                        if not is_cancelled:

                            pnr = group["pnr"]

                            def cancel_booking(
                                selected_pnr=pnr
                            ):

                                def perform_cancel():

                                    with db() as connection:

                                        with connection.cursor() as cursor:

                                            cursor.execute("""
                                                UPDATE bookings
                                                SET status = 'CANCELLED'
                                                WHERE pnr = %s
                                                  AND user_id = %s
                                                  AND status = 'CONFIRMED'
                                            """, (
                                                selected_pnr,
                                                app_state["user_id"]
                                            ))

                                        connection.commit()

                                    ui.notify(
                                        "Booking cancelled successfully.",
                                        type="positive"
                                    )

                                    ui.navigate.to("/bookings")

                                with ui.dialog() as dialog:

                                    with ui.card().classes(
                                        "p-6 rounded-2xl"
                                    ):

                                        ui.label(
                                            "Cancel this booking?"
                                        ).classes(
                                            "text-xl font-bold"
                                        )

                                        ui.label(
                                            f"PNR: {selected_pnr}"
                                        ).classes(
                                            "text-sm text-slate-500 mt-1"
                                        )

                                        ui.label(
                                            "All passengers under this PNR "
                                            "will be cancelled."
                                        ).classes(
                                            "text-sm text-slate-500 mt-2"
                                        )

                                        with ui.row().classes(
                                            "w-full justify-end gap-2 mt-5"
                                        ):

                                            ui.button(
                                                "Keep Booking",
                                                on_click=dialog.close
                                            ).props(
                                                "flat"
                                            )

                                            ui.button(
                                                "Cancel Booking",
                                                on_click=lambda: (
                                                    dialog.close(),
                                                    perform_cancel()
                                                )
                                            ).props(
                                                "unelevated color=negative"
                                            )

                                dialog.open()

                            ui.button(
                                "Cancel Booking",
                                icon="cancel",
                                on_click=cancel_booking
                            ).props(
                                "flat color=negative"
                            )


# ============================================================
# START APPLICATION
# ============================================================

if __name__ in {"__main__", "__mp_main__"}:

    print("Setting up RailGo database...")

    setup_database()

    print("Starting RailGo...")
    print("Open: http://localhost:5000")

    ui.run(
        host="0.0.0.0",
        port=5000,
        title="RailGo - Railway Booking",
        favicon="🚆"
    )