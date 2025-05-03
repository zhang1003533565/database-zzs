from django.db import models

class HealthOrganization(models.Model):
    # 字段定义
    xcyss = models.CharField(max_length=100, verbose_name="乡村医生数")
    zhen = models.CharField(max_length=100, verbose_name="镇")
    dsjzx_taskid = models.CharField(max_length=100, verbose_name="批次号")
    jhpt_update_time = models.CharField(max_length=100, verbose_name="时间戳")
    id = models.CharField(max_length=100, primary_key=True, verbose_name="主键")
    xzcs = models.CharField(max_length=100, verbose_name="行政村数")
    jhpt_delete = models.CharField(max_length=100, verbose_name="删除标识")

    def __str__(self):
        return f"{self.zhen} - {self.xcyss}"

    class Meta:
        verbose_name = '健康组织'
        verbose_name_plural = '健康组织'
        db_table = "health_organization"  # 自定义表名
