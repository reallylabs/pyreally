# Python Client for Really.io

```
import pyreally

really = pyreally.Really()
really.login_anonymous()
f = really.get("/users/1234")
print(f.result())
```

