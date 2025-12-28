import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


from analyzer.models.label_model import LabelKeywords



model = LabelKeywords()
model.get_X_y()
model.train()
print(model.predict('gender'))