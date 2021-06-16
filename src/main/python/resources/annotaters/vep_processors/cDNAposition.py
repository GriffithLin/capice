from src.main.python.resources.annotaters.vep_processors.template_position import TemplatePosition


class CDNAPosition(TemplatePosition):
    def __init__(self):
        super(CDNAPosition, self).__init__(
            name='cDNA_position',
            usable=True
        )

    @property
    def columns(self):
        return ['cDNApos', 'relcDNApos']
