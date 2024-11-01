import logging
import sys

root = logging.getLogger()
root.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)


from etiket_client.sync.run import run_sync_iter, sync_loop
from etiket_client.local.database import Session 

# sync only one dataset
with Session() as session:
  run_sync_iter(session)

# sync all datasets
sync_loop()
