import asyncio
import websockets
import asyncio
import websockets
import json
import mariadb
from mariadb import connect

# MariaDB configuration
db_config = {
    'host': 'localhost',
    'user': 'girmaaa',
    'password': '@Ritagirma123@',
    'database': 'stack4things'
}

# Function to handle database operations
async def execute_db_query(query, args=None):
    try:
        conn = await connect(**db_config)
        cursor = await conn.cursor()
        if args:
            await cursor.execute(query, args)
        else:
            await cursor.execute(query)
        if query.lower().startswith('select'):
            rows = await cursor.fetchall()
            return rows
        else:
            await conn.commit()
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
    finally:
        await cursor.close()
        await conn.close()

# WebSocket server handler and other functions remain the same as previously provided

