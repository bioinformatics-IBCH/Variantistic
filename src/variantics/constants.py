import enum


class VarianticsCommands(enum.Enum):
    PREPARE = 'prepare'
    CHECK_GZ = 'check_gz'
    CREATE_HISTOGRAMS = 'create_histograms'


SAMPLE_NAME_COLUMN = 'Sample name'

VARIANTICS_HIST_VCF_HEADER = {
    'ID': 'VARIANTICS_HIST',
    'Description': 'Dict of histograms',
    'Type': 'String',
    'Number': 1
}
