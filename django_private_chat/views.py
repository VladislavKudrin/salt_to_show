# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.http import Http404, HttpResponseForbidden
# from django.shortcuts import render
# from django.urls import reverse
# from django.views.generic.edit import FormMixin

# from django.views.generic import DetailView, ListView

# from .forms import ComposeForm
# from .models import Thread, ChatMessage


# class InboxView(LoginRequiredMixin, ListView):
#     template_name = 'django_private_chat/inbox.html'
#     def get_queryset(self):
#         return Thread.objects.by_user(self.request.user)


# class ThreadView(LoginRequiredMixin, FormMixin, DetailView):
#     template_name = 'django_private_chat/thread.html'
#     form_class = ComposeForm
#     success_url = './'

#     def get_queryset(self):
#         print('dawd')
#         return Thread.objects.by_user(self.request.user)

#     def get_object(self):
#         other_username  = self.kwargs.get("username")
#         print(other_username)
#         obj, created    = Thread.objects.get_or_new(self.request.user, other_username)
#         if obj == None:
#             raise Http404
#         return obj

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['form'] = self.get_form()
#         return context

#     def post(self, request, *args, **kwargs):
#         if not request.user.is_authenticated:
#             return HttpResponseForbidden()
#         self.object = self.get_object()
#         form = self.get_form()
#         if form.is_valid():
#             return self.form_valid(form)
#         else:
#             return self.form_invalid(form)

#     def form_valid(self, form):
#         thread = self.get_object()
#         user = self.request.user
#         message = form.cleaned_data.get("message")
#         ChatMessage.objects.create(user=user, thread=thread, message=message)
#         return super().form_valid(form)



# # from django.views import generic
# # from braces.views import LoginRequiredMixin

# # try:
# #     from django.urls import reverse
# # except ImportError:
# #     from django.core.urlresolvers import reverse
# # from . import models
# # from . import utils
# # from django.shortcuts import get_object_or_404, render
# # from django.contrib.auth import get_user_model
# # from django.conf import settings
# # from django.db.models import Q
# # from django.http import Http404


# # class DialogListView(LoginRequiredMixin, generic.ListView):
# #     template_name = 'django_private_chat/dialogs.html'
# #     model = models.Dialog
# #     ordering = 'modified'

# #     def get_queryset(self):
# #         dialogs = models.Dialog.objects.filter(Q(owner=self.request.user) | Q(opponent=self.request.user))
# #         return dialogs.order_by("-timestamp")

# #     def get_context_data(self, **kwargs):
# #         context = super().get_context_data()
# #         if self.kwargs.get('username'):
# #             # TODO: show alert that user is not found instead of 404
# #             user = get_object_or_404(get_user_model(), username=self.kwargs.get('username'))
# #             dialog = utils.get_dialogs_with_user(self.request.user, user)
# #             if len(dialog) == 0:
# #                 dialog = models.Dialog.objects.create(owner=self.request.user, opponent=user)
# #             else:
# #                 dialog = dialog[0]
# #             context['active_dialog'] = dialog
# #         else:
# #             context['active_dialog'] = self.object_list[0]
# #         if self.request.user == context['active_dialog'].owner:
# #             context['opponent_username'] = context['active_dialog'].opponent.username
# #         else:
# #             context['opponent_username'] = context['active_dialog'].owner.username
# #         context['ws_server_path'] = '{}://{}:{}/'.format(
# #             settings.CHAT_WS_SERVER_PROTOCOL,
# #             settings.CHAT_WS_SERVER_HOST,
# #             settings.CHAT_WS_SERVER_PORT,
# #         )
# #         context['opponent_picture'] = context['active_dialog'].opponent.profile_foto
# #         context['owner_picture'] = context['active_dialog'].owner.profile_foto
# #         return context
