def status_colored(status: str) -> str:
  status_colored = ""

  if status == "PENDING":
    status_colored = f"[bold yellow]{status}[/bold yellow]"
  elif status == "COMPLETED":
    status_colored = f"[bold green]{status}[/bold green]"
  else:
    status_colored = f"[bold red]{status}[/bold red]"

  return status_colored
