# TODO

## Plan confirmation
- [x] Gather current project state (read app.py, templates/index.html, static/script.js, static/style.css)
- [ ] Provide edit plan + enhance project

## Step 1: Fix broken frontend JS
- [ ] Repair `static/script.js` search handler (close braces, toggle display correctly)
- [ ] Make search work reliably (hide non-matching items, show matching items)
- [ ] Remove stray/incomplete code

## Step 2: Enhance UI/UX (no backend changes)
- [ ] Complete `static/style.css` (add missing closing braces and finish design)
- [ ] Add dark-mode styling for body/nav/buttons/task list
- [ ] Improve layout (container styling, task item spacing, hover effects)

## Step 3: Optional frontend improvements
- [ ] Improve delete UX (confirm prompt) without backend change

## Step 4: Validate
- [ ] Run `python app.py` and manually verify:
  - add task
  - delete task
  - search filtering
  - theme toggle


