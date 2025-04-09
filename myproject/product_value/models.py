from django.db import models

class ProductValue(models.Model):
    # 字段定义
    zb = models.CharField(max_length=100, verbose_name="指标")
    create_time = models.CharField(max_length=100, verbose_name="写入时间")
    jhpt_update_time = models.CharField(max_length=100, verbose_name="修改时间")
    dsjzx_taskid = models.CharField(max_length=100, verbose_name="批次号")
    id = models.CharField(max_length=100, primary_key=True, verbose_name="自增主键")
    zcz = models.CharField(max_length=100, verbose_name="现价总产值")
    jhpt_delete = models.CharField(max_length=100, verbose_name="逻辑删除")
    spl = models.CharField(max_length=100, verbose_name="商品率")
    spcz = models.CharField(max_length=100, verbose_name="商品产值")

    def __str__(self):
        return f"{self.zb} - {self.spl}"

    class Meta:
        verbose_name = "农业商品产值和商品率"
        verbose_name_plural = "农业商品产值和商品率"
        db_table = "product_value"  # 自定义表名
