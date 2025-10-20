import typer
import uuid
from rich.console import Console
from rich.table import Table
from typing import Literal
from rich import print
from src.database.connection.connect_database import connect_database
from src.database.helpers.status_colors import status_colored

# Conexión a la base de datos
conn = connect_database("./src/database/todo.db")

app = typer.Typer()
table = Table("UUID", "Name", "Description", "Status", show_lines=True)
console = Console()

STATUS = Literal["COMPLETED", "PENDING", "IN_PROGRESS"]

@app.command(short_help="Create on task")
def create(name: str, description: str, status: STATUS):
  if conn:
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO TASKS(uuid, name, description, status) VALUES(?, ?, ?, ?)",
        (str(uuid.uuid4()), name, description, status, )
    )
    conn.commit()
    conn.close()
    print("One task have been [bold green]created[/bold green]")

@app.command(short_help="List all tasks")
def list():
  if conn:
    cursor = conn.cursor()
    results = cursor.execute(
        "SELECT uuid, name, description, status FROM tasks"
    )
    for uuid, name, description, status in results.fetchall():
      status_with_color = status_colored(status)

      table.add_row(uuid, name, description, status_with_color)
    conn.close() # type: ignore

  table.caption = "List all tasks"
  console.print(table)

@app.command(short_help="Update one task")
def update():
  # "UPDATE TASKS SET name=?, description=?, status=? WHERE uuid = ?"
  print("update one task")
def update(task_id, name, description, status):
    """Actualiza una tarea existente"""
    if conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE TASKS SET name=?, description=?, status=? WHERE uuid=?",
            (name, description, status, task_id)
        )
        conn.commit()
        conn.close()
        print("One task have been [bold yellow]updated[/bold yellow]")    
@app.command(short_help="Delete one task")
def delete():
  # "DELETE FROM TASKS WHERE uuid = ?"
  print("delete one task")


if __name__ == "__main__":
  app()
  