from django.db import models

class TechApplication(models.Model):
    # 字段定义
    create_time = models.CharField(max_length=100, verbose_name="写入时间")
    dmsyl = models.CharField(max_length=100, verbose_name="地膜使用量")
    nysyl = models.CharField(max_length=100, verbose_name="农药使用量")
    sdjxhcd = models.CharField(max_length=100, verbose_name="机械化程度")
    id = models.CharField(max_length=100, primary_key=True, verbose_name="自增主键")
    dsjzx_taskid = models.CharField(max_length=100, verbose_name="批次号")
    jxhcd = models.CharField(max_length=100, verbose_name="机械化程度")
    jgmj = models.CharField(max_length=100, verbose_name="机械面积")
    sdjmj = models.CharField(max_length=100, verbose_name="水稻机械面积")
    jhpt_delete = models.CharField(max_length=100, verbose_name="逻辑删除")
    sdjscd = models.CharField(max_length=100, verbose_name="机械化程度")
    jhpt_update_time = models.CharField(max_length=100, verbose_name="修改时间")
    hfsul = models.CharField(max_length=100, verbose_name="化肥施用量")
    jz = models.CharField(max_length=100, verbose_name="镇")
    dmfgmj = models.CharField(max_length=100, verbose_name="地膜覆盖面积")
    jdjsmj = models.CharField(max_length=100, verbose_name="水稻机械收获面积")

    def __str__(self):
        return f"{self.jz} - {self.dmsyl}"

    class Meta:
        verbose_name = "农业技术应用"
        verbose_name_plural = "农业技术应用"
        db_table = "tech_application"  # 自定义表名
