from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import BookClub, ClubMembership, ClubDiscussion
from .forms import BookClubForm, ClubDiscussionForm


def clubs_list(request):
    """List all book clubs."""
    clubs = BookClub.objects.all().order_by('-created_at')
    paginator = Paginator(clubs, 12)
    page_number = request.GET.get('page')
    clubs = paginator.get_page(page_number)
    
    return render(request, 'clubs/clubs_list.html', {'clubs': clubs})


def club_detail(request, club_id):
    """Book club detail page."""
    club = get_object_or_404(BookClub, id=club_id)
    discussions = club.discussions.all().order_by('-created_at')[:10]
    
    # Check if user is a member
    is_member = False
    if request.user.is_authenticated:
        is_member = ClubMembership.objects.filter(
            user=request.user, 
            club=club
        ).exists()
    
    context = {
        'club': club,
        'discussions': discussions,
        'is_member': is_member,
    }
    
    return render(request, 'clubs/club_detail.html', context)


@login_required
def create_club(request):
    """Create a new book club."""
    if request.method == 'POST':
        form = BookClubForm(request.POST)
        if form.is_valid():
            club = form.save(commit=False)
            club.created_by = request.user
            club.save()
            
            # Add creator as admin member
            ClubMembership.objects.create(
                user=request.user,
                club=club,
                is_admin=True
            )
            
            messages.success(request, "Book club created successfully!")
            return redirect('club_detail', club_id=club.id)
    else:
        form = BookClubForm()
    
    return render(request, 'clubs/create_club.html', {'form': form})


@login_required
def join_club(request, club_id):
    """Join a book club."""
    club = get_object_or_404(BookClub, id=club_id)
    
    # Check if user is already a member
    membership, created = ClubMembership.objects.get_or_create(
        user=request.user,
        club=club
    )
    
    if created:
        messages.success(request, f"You've joined {club.name}!")
    else:
        messages.info(request, f"You're already a member of {club.name}.")
    
    return redirect('club_detail', club_id=club_id)


@login_required
def leave_club(request, club_id):
    """Leave a book club."""
    club = get_object_or_404(BookClub, id=club_id)
    
    try:
        membership = ClubMembership.objects.get(user=request.user, club=club)
        membership.delete()
        messages.success(request, f"You've left {club.name}.")
    except ClubMembership.DoesNotExist:
        messages.error(request, "You're not a member of this club.")
    
    return redirect('club_detail', club_id=club_id)


@login_required
def create_discussion(request, club_id):
    """Create a new discussion in a book club."""
    club = get_object_or_404(BookClub, id=club_id)
    
    # Check if user is a member
    if not ClubMembership.objects.filter(user=request.user, club=club).exists():
        messages.error(request, "You must be a member to create discussions.")
        return redirect('club_detail', club_id=club_id)
    
    if request.method == 'POST':
        form = ClubDiscussionForm(request.POST)
        if form.is_valid():
            discussion = form.save(commit=False)
            discussion.club = club
            discussion.user = request.user
            discussion.save()
            
            messages.success(request, "Discussion created successfully!")
            return redirect('club_detail', club_id=club_id)
    else:
        form = ClubDiscussionForm()
    
    return render(request, 'clubs/create_discussion.html', {
        'form': form,
        'club': club
    })


@login_required
def discussion_detail(request, discussion_id):
    """View a specific discussion."""
    discussion = get_object_or_404(ClubDiscussion, id=discussion_id)
    club = discussion.club
    
    # Check if user is a member of the club
    if not request.user in club.members.all():
        messages.error(request, "You must be a member of this club to view discussions.")
        return redirect('club_detail', club_id=club.id)
    
    context = {
        'discussion': discussion,
        'club': club,
    }
    return render(request, 'clubs/discussion_detail.html', context)
