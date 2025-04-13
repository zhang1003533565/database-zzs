import requests
import json
import pandas as pd


class QingpuAgricultureAPI:
    def __init__(self, token):
        self.api_url = "https://data.sh.gov.cn/interface/12224/36129"
        self.headers = {
            'content-type': 'application/json',
            'cache-control': 'no-cache',
            'token': token
        }
        self.timeout = 30

    def build_request(self, year=None, limit=20, offset=0):
        params = {
            "limit": limit,
            "offset": offset
        }
        if year:
            params["year"] = str(year)
        return params

    def make_request(self, params):
        try:
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=params,
                timeout=self.timeout
            )
            response.raise_for_status()
            data = response.json()

            if data.get('code') != '000000':
                return None, data.get('message', 'API返回错误')

            raw_data = data.get('data')

            if isinstance(raw_data, str):
                try:
                    result = json.loads(raw_data)
                except json.JSONDecodeError:
                    return None, "data字段JSON解析失败"
            else:
                result = raw_data

            if not result.get('state'):
                return None, result.get('message', '数据状态异常')

            records = result.get('data', [])
            return records, None

        except Exception as e:
            return None, f"请求异常: {str(e)}"

    def get_data_by_years(self, years=None, batch_size=100):
        all_data = []
        targets = years if years else [None]

        for year in targets:
            print(f"正在获取 {year} 年数据...")
            offset = 0
            while True:
                params = self.build_request(year, batch_size, offset)
                records, error = self.make_request(params)

                if error:
                    print(f"获取数据出错: {error}")
                    break
                if not records:
                    break

                all_data.extend(records)
                offset += len(records)

                if len(records) < batch_size:
                    break

        if not all_data:
            print("未获取到任何数据")
            return None

        return pd.DataFrame(all_data)

    def save_to_markdown(self, df, filename="农业历年总产值.md"):
        if df is None or df.empty:
            print("❌ 没有数据可保存为 Markdown")
            return

        try:
            df = df.sort_values(by="year")
            md_lines = [
                "# 农业历年总产值（1950-2025）\n",
                "| 年份 | 农业总产值(万元) | 种植业 | 渔业 | 牧业 | 林业 | 副业 | 农林牧渔服务业 | 修改时间 | 写入时间 | 逻辑删除 | 批次号 | 自增主键 |",
                "|------|------------------|--------|------|------|------|------|----------------|------------|------------|------------|--------|------------|"
            ]

            for _, row in df.iterrows():
                md_lines.append(
                    f"| {row.get('year', '-')} "
                    f"| {row.get('nyzcz', '-')} "
                    f"| {row.get('zzy', '-')} "
                    f"| {row.get('yy', '-')} "
                    f"| {row.get('my', '-')} "
                    f"| {row.get('ly', '-')} "
                    f"| {row.get('fy', '-')} "
                    f"| {row.get('nlmyfwy', '-')} "
                    f"| {row.get('jhpt_update_time', '-')} "
                    f"| {row.get('create_time', '-')} "
                    f"| {row.get('jhpt_delete', '-')} "
                    f"| {row.get('dsjzx_taskid', '-')} "
                    f"| {row.get('id', '-')} |"
                )

            with open(filename, "w", encoding="utf-8") as f:
                f.write("\n".join(md_lines))
                print(f"📄 Markdown 文件已保存为：{filename}")

        except Exception as e:
            print(f"保存 Markdown 文件失败: {str(e)}")


if __name__ == "__main__":
    TOKEN = "59f1c9bba4099db43bf707fc25d2d89f"
    api = QingpuAgricultureAPI(TOKEN)

    # 拉取 1950-2025 年份数据
    years = list(range(1978, 2026))
    df = api.get_data_by_years(years)

    if df is not None:
        print(f"\n✅ 成功获取 {len(df)} 条记录")
        api.save_to_markdown(df)
    else:
        print("❌ 未能获取有效数据")
