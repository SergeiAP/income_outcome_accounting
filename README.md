## 1. Create DB
```bash
python
from src.accounts.tables import Base
from src.accounts.database import engine
Base.metadata.create_all(engine)
quit()
```

## 2. Fill database

```bash
cd ./database && make fill_database
```
