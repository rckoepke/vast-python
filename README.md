# vast-python

Super basic git repo so interested folks can pull request. More to follow.

### Installation

```bash
python setup.py sdist
pip install dist/vast-0.1.0.tar.gz
```

### Useage

```python
from vast.api import VastAPI

VastAPI.set_api_key(KEY)
api = VastAPI()
api.search_offers(max_rows=5)
```

```bash
vast-ai set-api-key <KEY>
vast search-offers -m 5
```