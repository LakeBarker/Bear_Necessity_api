from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework import generics, status
from django.shortcuts import get_object_or_404

from ..models.timeline import Timeline
from ..serializers import TimelineSerializer

# Create your views here.
class Timelines(generics.ListCreateAPIView):
    permission_classes=(IsAuthenticated,)
    serializer_class = TimelineSerializer
    def get(self, request):
        """Index request"""
        # Get all the timelines:
        # timelines = Timeline.objects.all()
        # Filter the timelines by owner, so you can only see your owned timelines
        timelines = Timeline.objects.filter(owner=request.user.id)
        # Run the data through the serializer
        data = TimelineSerializer(timelines, many=True).data
        return Response({ 'timelines': data })

    def post(self, request):
        """Create request"""
        # Add user to request data object
        request.data['timeline']['owner'] = request.user.id
        # Serialize/create timeline
        timeline = TimelineSerializer(data=request.data['timeline'])
        # If the timeline data is valid according to our serializer...
        if timeline.is_valid():
            # Save the created timeline & send a response
            timeline.save()
            return Response({ 'timeline': timeline.data }, status=status.HTTP_201_CREATED)
        # If the data is not valid, return a response with the errors
        return Response(timeline.errors, status=status.HTTP_400_BAD_REQUEST)

class TimelineDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=(IsAuthenticated,)
    def get(self, request, pk):
        """Show request"""
        # Locate the timeline to show
        timeline = get_object_or_404(Timeline, pk=pk)
        # Only want to show owned timelines?
        if request.user != timeline.owner:
            raise PermissionDenied('Unauthorized, you do not own this timeline')

        # Run the data through the serializer so it's formatted
        data = TimelineSerializer(timeline).data
        return Response({ 'timeline': data })

    def delete(self, request, pk):
        """Delete request"""
        # Locate timeline to delete
        timeline = get_object_or_404(Timeline, pk=pk)
        # Check the timeline's owner against the user making this request
        if request.user != timeline.owner:
            raise PermissionDenied('Unauthorized, you do not own this timeline')
        # Only delete if the user owns the  timeline
        timeline.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def partial_update(self, request, pk):
        """Update Request"""
        # Locate Timeline
        # get_object_or_404 returns a object representation of our Timeline
        timeline = get_object_or_404(Timeline, pk=pk)
        # Check the timeline's owner against the user making this request
        if request.user != timeline.owner:
            raise PermissionDenied('Unauthorized, you do not own this timeline')

        # Ensure the owner field is set to the current user's ID
        request.data['timeline']['owner'] = request.user.id
        # Validate updates with serializer
        data = TimelineSerializer(timeline, data=request.data['timeline'], partial=True)
        if data.is_valid():
            # Save & send a 204 no content
            data.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        # If the data is not valid, return a response with the errors
        return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)
