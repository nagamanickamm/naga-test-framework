import os

from naga.test.framework.utils.common_utils import Utils
from naga.test.framework.utils.report_utils import ReportUtils

folder = os.getcwd()
diff = Utils.image_compare(folder + "/demo/test_suite/resources/images/AgeofGods.png", folder + "/demo/test_suite/resources/images/AgeofGods_1.png")

ReportUtils.log(diff)
