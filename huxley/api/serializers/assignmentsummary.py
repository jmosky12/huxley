# Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from rest_framework import serializers

from huxley.core.models import AssignmentSummary


class AssignmentSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = AssignmentSummary
        fields = (
        	'id', 
        	'name', 
        	'summary', 
        	'published_summary', 
        	'voting', 
        	'session_one',
        	'session_two',
        	'session_three',
        	'session_four'
    	)
