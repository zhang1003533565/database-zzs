from django.db import models

class TotalAgriculture(models.Model):
    # 字段定义
    dw = models.CharField(max_length=100, verbose_name="单位")
    nyzz = models.CharField(max_length=100, verbose_name="增长百分比")
    dsjzx_taskid = models.CharField(max_length=100, verbose_name="批次号")
    id = models.CharField(max_length=100, primary_key=True, verbose_name="自增主键")
    zbmc = models.CharField(max_length=100, verbose_name="指标名称")
    nyzcz = models.CharField(max_length=100, verbose_name="季度")
    jhpt_delete = models.CharField(max_length=100, verbose_name="逻辑删除")
    jhpt_update_time = models.CharField(max_length=100, verbose_name="时间戳")
    create_time = models.CharField(max_length=100, verbose_name="写入时间")

    def __str__(self):
        return f"{self.zbmc} - {self.nyzcz}"

    class Meta:
        verbose_name = "农业总产值"
        verbose_name_plural = "农业总产值"
        db_table = "total_agriculture"  # 自定义表名
