from django.db import models

class RuralOrganization(models.Model):
    # 字段定义
    jz = models.CharField(max_length=100, verbose_name="镇")
    cmxz = models.CharField(max_length=100, verbose_name="村民小组")
    ncrk = models.CharField(max_length=100, verbose_name="农村人口")
    create_time = models.CharField(max_length=100, verbose_name="写入时间")
    cmwyh = models.CharField(max_length=100, verbose_name="村民委员会")
    dsjzx_taskid = models.CharField(max_length=100, verbose_name="批次号")
    ncjzrk = models.CharField(max_length=100, verbose_name="其中农村居民口")
    jhpt_delete = models.CharField(max_length=100, verbose_name="逻辑删除")
    ncjzhs = models.CharField(max_length=100, verbose_name="其中农村居民户数")
    jhpt_update_time = models.CharField(max_length=100, verbose_name="修改时间")
    id = models.CharField(max_length=100, primary_key=True, verbose_name="自增主键")

    def __str__(self):
        return f"{self.jz} - {self.cmxz}"

    class Meta:
        verbose_name = "农村基层数据"
        verbose_name_plural = "农村基层数据"
        db_table = "rural_organization"  # 自定义表名
