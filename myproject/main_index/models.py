from django.db import models

class MainIndex(models.Model):
    # 字段定义
    id = models.CharField(max_length=100, primary_key=True, verbose_name="自增主键")
    jhpt_delete = models.CharField(max_length=100, verbose_name="逻辑删除")
    dw = models.CharField(max_length=100, verbose_name="单位")
    jhpt_update_time = models.CharField(max_length=100, verbose_name="修改时间")
    create_time = models.CharField(max_length=100, verbose_name="写入时间")
    ze_last_year = models.CharField(max_length=100, verbose_name="比去年增长")
    dsjzx_taskid = models.CharField(max_length=100, verbose_name="批次号")
    ze2023 = models.CharField(max_length=100, verbose_name="2023年")
    zb = models.CharField(max_length=100, verbose_name="指标")

    def __str__(self):
        return f"{self.zb} - {self.ze2023}"

    class Meta:
        verbose_name = "农业主要指标"
        verbose_name_plural = "农业主要指标"
        db_table = "main_index"  # 自定义表名
