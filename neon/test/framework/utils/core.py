from naga.test.framework.utils.common_utils import CommonUtils
from naga.test.framework.utils.date_utils import DateUtils
from naga.test.framework.utils.db_utils import DBUtils
from naga.test.framework.utils.encryption import Encryption
from naga.test.framework.utils.file_utils import FileUtils
from naga.test.framework.utils.json_utils import JsonUtils
from naga.test.framework.utils.list_utils import ListUtils
from naga.test.framework.utils.regex_utils import RegEx
from naga.test.framework.utils.report_utils import ReportUtils
from naga.test.framework.utils.spec_html_utils import SpecHTMLUtils
from naga.test.framework.utils.xml_utils import XMLUtils


class Core(CommonUtils, FileUtils, JsonUtils, DateUtils, DBUtils, ListUtils, XMLUtils, RegEx, ReportUtils, SpecHTMLUtils, Encryption):
    pass
