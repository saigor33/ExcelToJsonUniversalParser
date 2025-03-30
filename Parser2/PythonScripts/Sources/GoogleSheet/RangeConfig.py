from typing import Optional


class RangeConfig:
    def __init__(
            self,
            id: str,
            sheet_name: str,
            start_column_name: str,
            end_column_name: str,
            start_row_index: int,
            end_row_index: Optional[int]
    ):
        self.id = id
        self.sheet_name = sheet_name
        self.start_column_name = start_column_name
        self.end_column_name = end_column_name
        self.start_row_index = start_row_index
        self.end_row_index = end_row_index
