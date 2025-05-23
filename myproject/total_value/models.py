from django.db import models

class TotalValue(models.Model):
    # 字段定义
    yy = models.CharField(max_length=100, verbose_name="渔业", null=True, blank=True)
    fy = models.CharField(max_length=100, verbose_name="副业", null=True, blank=True)
    jhpt_update_time = models.CharField(max_length=100, verbose_name="修改时间")
    nlmyfwy = models.CharField(max_length=100, verbose_name="农林牧渔服务业", null=True, blank=True)
    id = models.CharField(max_length=100, primary_key=True, verbose_name="自增主键")
    jhpt_delete = models.CharField(max_length=100, verbose_name="逻辑删除", null=True, blank=True)
    ly = models.CharField(max_length=100, verbose_name="林业", null=True, blank=True)
    create_time = models.CharField(max_length=100, verbose_name="写入时间")
    dsjzx_taskid = models.CharField(max_length=100, verbose_name="批次号")
    year = models.CharField(max_length=100, verbose_name="年份")
    my = models.CharField(max_length=100, verbose_name="牧业", null=True, blank=True)
    zzy = models.CharField(max_length=100, verbose_name="种植业", null=True, blank=True)
    nyzcz = models.CharField(max_length=100, verbose_name="农业总产值", null=True, blank=True)

    def __str__(self):
        return f"{self.year} - {self.nyzcz}"

    class Meta:
        verbose_name = "农业历年总产值"
        verbose_name_plural = "农业历年总产值"
        db_table = "total_value"  # 自定义表名
