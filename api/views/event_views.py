from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework import generics, status
from django.shortcuts import get_object_or_404

from ..models.event import Event
from ..serializers import EventSerializer

# Create your views here.
class Events(generics.ListCreateAPIView):
    permission_classes=(IsAuthenticated,)
    serializer_class = EventSerializer
    def get(self, request):
        """Index request"""
        # Get all the events:
        # events = Event.objects.all()
        # Filter the events by owner, so you can only see your owned events
        events = Event.objects.filter(owner=request.user.id)
        # Run the data through the serializer
        data = EventSerializer(events, many=True).data
        return Response({ 'events': data })

    def post(self, request):
        """Create request"""
        # Add user to request data object
        request.data['event']['owner'] = request.user.id
        # Serialize/create event
        event = EventSerializer(data=request.data['event'])
        # If the event data is valid according to our serializer...
        if event.is_valid():
            # Save the created event & send a response
            event.save()
            return Response({ 'event': event.data }, status=status.HTTP_201_CREATED)
        # If the data is not valid, return a response with the errors
        return Response(event.errors, status=status.HTTP_400_BAD_REQUEST)

class EventDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=(IsAuthenticated,)
    def get(self, request, pk):
        """Show request"""
        # Locate the event to show
        event = get_object_or_404(Event, pk=pk)
        # Only want to show owned events?
        if request.user != event.owner:
            raise PermissionDenied('Unauthorized, you do not own this event')

        # Run the data through the serializer so it's formatted
        data = EventSerializer(event).data
        return Response({ 'event': data })

    def delete(self, request, pk):
        """Delete request"""
        # Locate event to delete
        event = get_object_or_404(Event, pk=pk)
        # Check the event's owner against the user making this request
        if request.user != event.owner:
            raise PermissionDenied('Unauthorized, you do not own this event')
        # Only delete if the user owns the  event
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def partial_update(self, request, pk):
        """Update Request"""
        # Locate Event
        # get_object_or_404 returns a object representation of our Event
        event = get_object_or_404(Event, pk=pk)
        # Check the event's owner against the user making this request
        if request.user != event.owner:
            raise PermissionDenied('Unauthorized, you do not own this event')

        # Ensure the owner field is set to the current user's ID
        request.data['event']['owner'] = request.user.id
        # Validate updates with serializer
        data = EventSerializer(event, data=request.data['event'], partial=True)
        if data.is_valid():
            # Save & send a 204 no content
            data.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        # If the data is not valid, return a response with the errors
        return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)
