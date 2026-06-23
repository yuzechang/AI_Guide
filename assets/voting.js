/* ===== AI Nav – 工具投票系统 ===== */
const VOTES_KEY = 'ainav_votes';

function getVotes() {
  return JSON.parse(localStorage.getItem(VOTES_KEY) || '{}');
}

function getVote(toolId) {
  return getVotes()[toolId] || null;
}

function setVote(toolId, direction) {
  var votes = getVotes();
  if (votes[toolId] === direction) {
    delete votes[toolId];
  } else {
    votes[toolId] = direction;
  }
  localStorage.setItem(VOTES_KEY, JSON.stringify(votes));
  return votes[toolId] || null;
}

function initVoting(toolId) {
  var upBtn = document.getElementById('voteUp');
  var downBtn = document.getElementById('voteDown');
  if (!upBtn || !downBtn) return;

  var current = getVote(toolId);
  updateVoteBtns(upBtn, downBtn, current);

  upBtn.addEventListener('click', function() {
    var newVote = setVote(toolId, 'up');
    updateVoteBtns(upBtn, downBtn, newVote);
  });
  downBtn.addEventListener('click', function() {
    var newVote = setVote(toolId, 'down');
    updateVoteBtns(upBtn, downBtn, newVote);
  });
}

function updateVoteBtns(upBtn, downBtn, vote) {
  upBtn.classList.toggle('vote-active-up', vote === 'up');
  downBtn.classList.toggle('vote-active-down', vote === 'down');
  upBtn.title = vote === 'up' ? 'Remove helpful vote' : 'Mark as helpful';
  downBtn.title = vote === 'down' ? 'Remove vote' : 'Mark as not helpful';
}
