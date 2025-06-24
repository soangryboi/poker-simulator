import pandas as pd
from typing import Dict, Optional

class PushFoldChart:
    def __init__(self, csv_path: str, stack_col: Optional[str] = None):
        self.chart = self._parse_csv(csv_path, stack_col)

    def _parse_csv(self, csv_path: str, stack_col: Optional[str] = None) -> Dict[int, Dict[str, bool]]:
        df = pd.read_csv(csv_path)
        # 스택 컬럼 자동 감지
        if stack_col is None:
            for col in df.columns:
                if col.lower() in ['stack', 'bb', 'bb_stack', 'stacks']:
                    stack_col = col
                    break
        if stack_col is None:
            raise ValueError('스택 컬럼(Stack/BB 등)을 찾을 수 없습니다.')
        hand_col = 'Hand' if 'Hand' in df.columns else df.columns[0]
        chart = {}
        # 세로 구조: 각 행이 (stack, hand, value)
        if len(df.columns) == 3:
            for _, row in df.iterrows():
                stack = int(float(row[stack_col]))
                hand = str(row[hand_col]).strip()
                value = PushFoldChart._to_bool(row[df.columns.difference([stack_col, hand_col])[0]])
                if stack not in chart:
                    chart[stack] = {}
                chart[stack][hand] = value
        # 가로 구조: 첫 컬럼이 hand, 나머지가 stack별 값
        else:
            for _, row in df.iterrows():
                hand = str(row[hand_col]).strip()
                for col in df.columns:
                    if col == hand_col:
                        continue
                    try:
                        stack = int(float(col))
                    except Exception:
                        continue
                    value = PushFoldChart._to_bool(row[col])
                    if stack not in chart:
                        chart[stack] = {}
                    chart[stack][hand] = value
        return chart

    @staticmethod
    def _to_bool(val):
        if isinstance(val, str):
            val = val.strip().upper()
            if val in ['1', 'Y', 'YES', 'TRUE', 'T', 'PUSH']:
                return True
            if val in ['0', 'N', 'NO', 'FALSE', 'F', 'FOLD']:
                return False
        if isinstance(val, (int, float)):
            return bool(val)
        return False

    def should_push(self, hand: str, stack: int) -> bool:
        return self.chart.get(stack, {}).get(hand, False)

# 사용 예시
if __name__ == '__main__':
    chart = PushFoldChart('../holdemresources_hu_push_int.csv')
    print(chart.should_push('AKs', 10))  # 10BB에서 AKs 푸시 여부
    print(chart.should_push('72o', 5))   # 5BB에서 72o 푸시 여부 