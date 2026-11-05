<div align="center">

# Debugging with the Zed Editor

**Attach Zed's debugger to small services and track down deliberate bugs.**

![Java 21](https://img.shields.io/badge/Java-21-orange)
![Quarkus 3.40.1](https://img.shields.io/badge/Quarkus-3.40.1-blue)
![Python 3](https://img.shields.io/badge/Python-3-yellow)
![FastAPI](https://img.shields.io/badge/FastAPI-009688)
![Zed](https://img.shields.io/badge/Editor-Zed-purple)

</div>

## Services

<details>
<summary><strong>Java service (Quarkus)</strong></summary>

### How it works

```mermaid
flowchart LR
    client[curl or RapiDoc] <-->|port 8080| jvm[Quarkus JVM]
    zed[Zed debugger] <-->|port 5005| jvm
```

### Quick start

Requires JDK 21 and Maven.

```bash
cd "java service"
mvn quarkus:dev
```

| URL | Purpose |
|---|---|
| http://localhost:8080/docs | API explorer (RapiDoc, needs internet) |
| http://localhost:8080/total?prices=10&prices=20&prices=30&discount=10 | Returns `60.0`, should be `54.0` |

<details>
<summary><strong>Debugging guide (click to show or hide)</strong></summary>

### 1. Set up Zed

1. Press `ctrl-shift-x` and install the **Java** extension.
2. Open the folder containing `pom.xml`:

   ```bash
   cd "java service"
   zed .
   ```

Recent JDTLS (the extension's language server) needs Java 25+, even though the service runs on 21. If you don't have it, add this to `~/.config/zed/settings.json`:

```json
{
  "lsp": {
    "jdtls": {
      "settings": {
        "jdk_auto_download": true
      }
    }
  }
}
```

### 2. Add `.zed/debug.json`

Create it inside `java service/`:

```json
[
  {
    "label": "Attach to Quarkus (port 5005)",
    "adapter": "Java",
    "request": "attach",
    "hostName": "localhost",
    "port": 5005
  }
]
```

- `[ ]` holds the list of configurations and is required, even for just one.
- `{ }` is one configuration.

### 3. Attach

1. Run `mvn quarkus:dev` and wait for `Listening for transport dt_socket at address: 5005`.
2. Press `f4` and choose **Attach to Quarkus (port 5005)**.

### 4. Set a breakpoint

Click the gutter or press `f9` on these lines:

| File | Line | Code | Meaning |
|---|---|---|---|
| `src/PriceResource.java` | 18 | `return priceService.total(prices, discount);` | Stops before calling the service, to check the input |
| `src/PriceService.java` | 8 | `int subtotal = 0;` | Stops at the start of the calculation |

### 5. Find the bug

1. Open http://localhost:8080/docs and send `GET /total` with `prices` 10, 20, 30 and `discount` 10.
2. The response stays pending while the code is paused. That's normal.
3. At `PriceResource.java:18`, check the input, then press `f5` (continue) to reach `PriceService.java:8`.
4. Step with `f10` (over) and watch the variables until one is wrong.

### Step actions

| Action | Key | What it does |
|---|---|---|
| Step over | `f10` | Runs the whole line, including any method it calls, then stops on the next line |
| Step into | `f11` | Goes inside the method being called and stops on its first line |
| Step out | `shift-f11` | Finishes the current method and stops back where it was called |
| Continue | `f5` | Runs until the next breakpoint, or until the request finishes |

In your code, suppose you're paused at line 18 of `PriceResource.java`:

```java
return priceService.total(prices, discount);
```

- **Step over:** `total()` runs completely, with its loop and calculation happening without a stop. You don't see any of it unless a breakpoint inside it is hit.
- **Step into:** you land in `PriceService_ClientProxy`, a class Quarkus generates between your two classes, not in `total()`. Stepping into again goes deeper into Quarkus code.
- **Continue:** use this to reach your own code. It stops at the breakpoint on `PriceService.java:8`, and also gets you out if you end up in Quarkus code.
- **Step out:** once inside `total()`, this runs the rest of the method and takes you back towards line 18. If you stop in `PriceService_ClientProxy` first, step out again.

</details>

<details>
<summary><strong>What I did (shows the bug, click to show or hide)</strong></summary>

The correct answer for `prices` 10, 20, 30 and `discount` 10 is `54.0`. **The highlighted line hasn't run yet**, so its result only shows up after your next action.

#### 1. Send the request

Execution stops at `PriceResource.java:18`, and the response stays pending, which is normal.

| Variable | Expected |
|---|---|
| `prices` | `[10, 20, 30]` |
| `discount` | `10` |

#### 2. Continue

You stop at `PriceService.java:8`. `prices` and `discountPercent` are visible, but `subtotal` doesn't exist yet.

Don't use Step into here, because it takes you into Quarkus's generated code.

#### 3. Step over through the method

| Action | Now stopped on | `price` | `subtotal` | `discount` |
|---|---|---|---|---|
| Step over | 9 `for` | – | `0` | – |
| Step over | 10 `subtotal += price` | `10` | `0` | – |
| Step over | 9 `for` | – | `10` | – |
| Step over | 10 | `20` | `10` | – |
| Step over | 9 `for` | – | `30` | – |
| Step over | 10 | `30` | `30` | – |
| Step over | 9 `for` | – | `60` | – |
| Step over | 13 `double discount = ...` | – | `60` | – |
| Step over | 14 `return ...` | – | `60` | **`0.0`, should be `6.0`** |

The last row is the bug: the loop is correct, and line 13 is the first line to produce a wrong value.

#### 4. Step out

The rest of `total()` runs, and you head back to `PriceResource.java:18`. If you stop in `PriceService_ClientProxy` first, Step out again. The response is still pending.

#### 5. Continue

The request finishes and RapiDoc shows `60.0`, which matches the `discount` of `0.0` you saw.

#### 6. After the fix

Change `100` to `100.0` on line 13, save and send the request again. Repeat the same actions. Everything is the same until line 14, where `discount` is now `6.0`, and the response is `54.0`.

#### If you end up in Quarkus code

Press **Continue** if your breakpoint on line 8 is still ahead of you. Your code is the frames with your own file names in the call stack, and anything with a `jdt://` path or `unknown` isn't yours.

</details>

</details>

<details>
<summary><strong>Python service (FastAPI)</strong></summary>

### How it works

```mermaid
flowchart LR
    client[Browser or curl] <-->|port 8000| app[FastAPI app]
    zed[Zed debugger] <-->|debugpy| app
```

Zed starts this service itself, so don't run it in a terminal while debugging.

### Quick start

Requires Python 3. Create the environment once:

```bash
cd "python service"
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

| URL | Purpose |
|---|---|
| http://localhost:8000/docs | API explorer (built into FastAPI) |
| http://localhost:8000/order?item=apple | Creates an order and should return one item |

<details>
<summary><strong>Debugging guide (click to show or hide)</strong></summary>

### 1. Open the repo root in Zed

```bash
zed .
```

No extension is needed, because Python debugging is built into Zed.

### 2. Check `.zed/debug.json`

Each configuration is one `{ }` in the list. This is the Python one:

```json
{
  "label": "Run Python service (port 8000)",
  "adapter": "Debugpy",
  "request": "launch",
  "module": "uvicorn",
  "args": ["main:app", "--port", "8000"],
  "cwd": "$ZED_WORKTREE_ROOT/python service",
  "python": "$ZED_WORKTREE_ROOT/python service/.venv/bin/python"
}
```

| Field | Meaning |
|---|---|
| `request` | `launch` makes Zed start the service |
| `module`, `args` | Runs `uvicorn main:app --port 8000` |
| `cwd` | The folder containing `main.py` |
| `python` | Uses the service's virtual environment |

### 3. Start the service

Press `f4` and choose **Run Python service (port 8000)**.

### 4. Set a breakpoint

Click the gutter or press `f9` on these lines:

| File | Line | Code | Meaning |
|---|---|---|---|
| `python service/main.py` | 10 | `return build_order(item)` | Stops before calling `build_order`, to check the input |
| `python service/orders.py` | 2 | `items.append(item)` | Stops before the item is added |

### 5. Find the bug

1. Open http://localhost:8000/docs and send `GET /order` with `item` set to `apple`. Each request should create a new order with one item.
2. The response stays pending while the code is paused. That's normal.
3. Press `f5` (continue) until the response arrives.
4. Send `GET /order` again with `item` set to `banana`.
5. Step with `f10` (over) and watch the variables until one is wrong.

### Step actions

| Action | Key | What it does |
|---|---|---|
| Step over | `f10` | Runs the whole line, including any method it calls, then stops on the next line |
| Step into | `f11` | Goes inside the function being called |
| Step out | `shift-f11` | Finishes the current function and stops back where it was called |
| Continue | `f5` | Runs until the next breakpoint, or until the request finishes |

</details>

<details>
<summary><strong>What I did (shows the bug, click to show or hide)</strong></summary>

Each order should contain only the item you just sent. **The highlighted line hasn't run yet**, so its result only shows up after your next action.

#### 1. First request: `item=apple`

| Action | Now stopped on | `item` | `items` |
|---|---|---|---|
| Send the request | `main.py:10` | `apple` | – |
| Continue | `orders.py:2` | `apple` | `[]` |
| Step over | `orders.py:3` | `apple` | `['apple']` |
| Continue | Request finishes | – | – |

The response is `{"items":["apple"],"count":1}`, which is correct.

#### 2. Second request: `item=banana`

| Action | Now stopped on | `item` | `items` |
|---|---|---|---|
| Send the request | `main.py:10` | `banana` | – |
| Continue | `orders.py:2` | `banana` | **`['apple']`, should be `[]`** |
| Step over | `orders.py:3` | `banana` | `['apple', 'banana']` |
| Continue | Request finishes | – | – |

The response is `{"items":["apple","banana"],"count":2}`, which is wrong.

`items` already holds `apple` before anything is added. Python creates the default `items=[]` once, when the function is defined, so every call shares the same list.

#### 3. The fix

Change `orders.py` and save:

```python
def build_order(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return {"items": items, "count": len(items)}
```

Stop the debugger with `shift-f5`, because this config doesn't reload code. Press `f4` to start again, then send both requests. Each response now has one item and a count of 1.

</details>

</details>
