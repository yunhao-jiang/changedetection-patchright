import sys
import patchright
import patchright.async_api
import patchright._impl._errors

sys.modules["playwright"] = patchright
sys.modules["playwright.async_api"] = patchright.async_api
sys.modules["playwright._impl._errors"] = patchright._impl._errors