"""
This module handles filename creation and serving.
"""

import os
from django.conf import settings


def filename_for_company(company_name):
	"""Return the filename for a company."""
	filename = fileify_company_name(company_name) + '.json'
	filename = os.path.join('/tmp', filename)
	return filename


def fileify_company_name(company_name):
	"""Make filename friendly version of company name."""
	return ''.join(s for s in company_name if s.isalnum())