from django.core.exceptions import FieldError
from django.http import Http404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from subscribe.serializers import FollowerSerializer, BlockPendinSerializer
from rest_framework.response import Response
from account.models import CustomUser


class FollowUnfollowView(APIView):
    permission_classes = [IsAuthenticated]

    def current_profile(self):
        try:
            return CustomUser.objects.get(id=self.request.user.id)
        except CustomUser.DoesNotExist:
            raise Http404

    def other_profile(self, pk):
        try:
            return CustomUser.objects.get(id=pk)
        except CustomUser.DoesNotExist:
            raise Http404

    def post(self, request, format=None):

        pk = request.data.get('id')  # Here pk is opposite user's profile ID
        req_type = request.data.get('type')

        current_profile = self.current_profile()
        if current_profile is None:
            return Response({'msg: Вы не авторизованы'})
        other_profile = self.other_profile(pk)

        if req_type == 'follow':
            if other_profile.private_account:
                other_profile.panding_request.add(current_profile)
                return Response({"Requested": "Follow request has been send!!"}, status=status.HTTP_200_OK)
            else:
                if other_profile.blocked_user.filter(id=current_profile.id).exists():
                    return Response(
                        {"Following Fail": "You can not follow this profile because your ID blocked by this user!!"},
                        status=status.HTTP_400_BAD_REQUEST)
                current_profile.following.add(other_profile)
                other_profile.followers.add(current_profile)
                return Response({"Following": "Following success!!"}, status=status.HTTP_200_OK)

        elif req_type == 'accept':
            current_profile.followers.add(other_profile)
            other_profile.following.add(current_profile)
            current_profile.panding_request.remove(other_profile)
            return Response({"Accepted": "Follow request successfuly accespted!!"}, status=status.HTTP_200_OK)

        elif req_type == 'decline':
            current_profile.panding_request.remove(other_profile)
            return Response({"Decline": "Follow request successfully declined!!"}, status=status.HTTP_200_OK)

        elif req_type == 'unfollow':
            current_profile.following.remove(other_profile)
            other_profile.followers.remove(current_profile)
            return Response({"Unfollow": "Unfollow success!!"}, status=status.HTTP_200_OK)

        elif req_type == 'remove':  # You can remove your follower
            current_profile.followers.remove(other_profile)
            other_profile.following.remove(current_profile)
            return Response({"Remove Success": "Successfuly removed your follower!!"}, status=status.HTTP_200_OK)

    # Here we can fetch followers,following detail and blocked user,pending request,sended request..

    def patch(self, request, format=None):

        req_type = request.data.get('type')

        if req_type == 'follow_detail':
            serializer = FollowerSerializer(self.current_profile())
            return Response({"data": serializer.data}, status=status.HTTP_200_OK)

        elif req_type == 'block_pending':
            serializer = BlockPendinSerializer(self.current_profile())
            pf = list(
                CustomUser.objects.filter(panding_request=self.current_profile().id).values('id', 'user__username',
                                                                                            'profile_pic',
                                                                                            'overall_pr'))
            return Response({"data": serializer.data, "Sended Request": pf}, status=status.HTTP_200_OK)

    # You can block and unblock user

    def put(self, request, format=None):
        pk = request.data.get('id')  # Here pk is oppisite user's profile ID
        req_type = request.data.get('type')

        if req_type == 'block':
            self.current_profile().blocked_user.add(self.other_profile(pk))
            return Response({"Blocked": "This user blocked successfuly"}, status=status.HTTP_200_OK)
        elif req_type == 'unblock':
            self.current_profile().blocked_user.remove(self.other_profile(pk))
            return Response({"Unblocked": "This user unblocked successfuly"}, status=status.HTTP_200_OK)
