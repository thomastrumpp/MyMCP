from mcp_server.server import add

print(f"Type: {type(add)}")
print(f"Dir: {dir(add)}")
try:
    print(f"Fn: {add.fn}")
except Exception:
    pass
