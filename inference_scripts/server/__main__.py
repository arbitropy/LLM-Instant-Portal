"""Example FastAPI server for model_instance.

To run this example:

```
python3 -m model_instance.server
```

or

```
uvicorn model_instance.server.app:app --reload
```

Then visit http://localhost:8000/docs to see the interactive API docs.

"""
import os
import argparse

import uvicorn

from model_instance.server.app import create_app, Settings

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    for name, field in Settings.model_fields.items():
        description = field.description
        if field.default is not None and description is not None:
            description += f" (default: {field.default})"
        parser.add_argument(
            f"--{name}",
            dest=name,
            type=field.annotation if field.annotation is not None else str,
            help=description,
        )

    args = parser.parse_args()
    settings = Settings(**{k: v for k, v in vars(args).items() if v is not None})
    app = create_app(settings=settings)

    uvicorn.run(
        app,
        host=os.getenv("HOST", settings.host),
        port=int(os.getenv("PORT", settings.port)),
    )
