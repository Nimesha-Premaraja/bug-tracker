# PDF Export Feature - Testing & Verification Guide

## Pre-Testing Setup

### 1. Install Dependencies
```bash
cd /Users/nimeshadilshan/Documents/github/nimeshadil/bug-tracking-system

# Install new dependency
pip install reportlab==4.0.7

# Or reinstall all requirements
pip install -r requirements.txt
```

### 2. Start the Application
```bash
# Using Docker Compose (Recommended)
docker-compose down
docker-compose up -d --build

# Or local development
export FLASK_APP=wsgi.py
export FLASK_ENV=development
flask run
```

### 3. Access the Application
- Frontend: http://localhost:5000
- Default credentials:
  - Admin: `admin@example.com` / `password123`
  - Developer: `dev@example.com` / `password123`
  - Tester: `tester@example.com` / `password123`

---

## Testing Scenarios

### Test 1: Basic PDF Export (Current Page)
**Steps**:
1. Login as any user
2. Navigate to `/bugs/` (Bugs page)
3. Verify "Export to PDF" button appears in top-right
4. Click "Export to PDF" button
5. Modal opens with two options
6. Verify "Current Page Only" is selected
7. Verify bug count shown (e.g., "5 bugs on this page")
8. Click "Export" button
9. Verify loading indicator appears
10. Verify PDF downloads as `BugReport_YYYY-MM-DD.pdf`
11. Open PDF and verify:
    - Title: "BUG REPORT"
    - Report date and username displayed
    - All bugs from current page included
    - Bug details are correct (title, status, priority, etc.)

**Expected Result**: ✅ PDF downloads successfully

---

### Test 2: Export All Results
**Steps**:
1. On bugs list page, apply filters:
   - Search: "login"
   - Status: "open"
2. Click "Export to PDF"
3. Select "All Results" radio button
4. Verify total count shown (e.g., "23 bugs matching filters")
5. If >400 bugs: verify warning message appears
6. Click "Export"
7. Verify PDF downloads
8. Open PDF and verify:
    - Report summary shows applied filters
    - All matching bugs included (not just current page)
    - Filters listed: Search, Status, Priority, Assignee

**Expected Result**: ✅ All filtered bugs included in PDF

---

### Test 3: Filter Combinations
**Steps**:
1. Apply multiple filters:
   - Status: "in_progress"
   - Priority: "high"
   - Assignee: Select a user
2. Click "Export to PDF"
3. Select "All Results"
4. Click "Export"
5. Verify PDF includes only bugs matching ALL filters
6. Verify report summary lists all applied filters

**Expected Result**: ✅ PDF correctly filters by all criteria

---

### Test 4: Search Query Export
**Steps**:
1. Enter search term: "button" or "crash" or any relevant term
2. Verify filtered results shown
3. Click "Export to PDF"
4. Export current page
5. Open PDF and verify search term in report summary
6. Verify only matching bugs included

**Expected Result**: ✅ Search filters applied to PDF

---

### Test 5: Large Export Handling
**Steps**:
1. Create/ensure there are >400 bugs in the system (or adjust filter)
2. Click "Export to PDF"
3. Select "All Results"
4. Verify warning appears: "Exporting X bugs. This may take a moment."
5. Click "Export"
6. Monitor for reasonable response time (<30 seconds)
7. Verify PDF downloads (may be large file)
8. Verify PDF has multiple pages with page breaks

**Expected Result**: ✅ Large export handled gracefully

---

### Test 6: Empty Results Export
**Steps**:
1. Apply restrictive filter: Status="closed", Priority="critical", Assignee="User With No Assignments"
2. Verify no bugs displayed
3. Click "Export to PDF"
4. Click "Export"
5. Verify flash message: "No bugs found to export."
6. Verify redirected to bug list page

**Expected Result**: ✅ Graceful handling of empty results

---

### Test 7: Permission Testing (Authentication)
**Steps**:
1. Logout of application
2. Try to access `/bugs/export-pdf` directly (POST request)
3. Verify redirected to login page

**Alternative**: Try accessing URL in browser dev tools
```javascript
// In browser console on bugs page
fetch('/bugs/export-pdf', { method: 'POST' })
```

**Expected Result**: ✅ Requires authentication

---

### Test 8: All User Roles Can Export
**Steps**:
1. Test with Admin user: Export should work ✅
2. Test with Developer user: Export should work ✅
3. Test with Tester user: Export should work ✅

**Expected Result**: ✅ All roles can export

---

### Test 9: Modal Functionality
**Steps**:
1. Click "Export to PDF"
2. Modal opens - verify styling looks good
3. Verify radio buttons work (click each option)
4. Click "Cancel" - verify modal closes
5. Click "Export to PDF" again
6. Click the X button (close) - verify modal closes
7. Click "Export to PDF" again
8. Click outside modal - verify modal closes

**Expected Result**: ✅ Modal opens/closes properly

---

### Test 10: PDF Content Accuracy
**Steps**:
1. Export a single page (1-3 bugs)
2. Open PDF and verify for each bug:
   - ✅ Bug ID matches
   - ✅ Title is correct
   - ✅ Description included
   - ✅ Status displayed correctly
   - ✅ Priority displayed correctly
   - ✅ Reporter email correct
   - ✅ Assignee email correct (or "Unassigned")
   - ✅ Created date format: YYYY-MM-DD HH:MM
   - ✅ Updated date format: YYYY-MM-DD HH:MM
   - ✅ Comments count correct
   - ✅ Attachments count correct

**Expected Result**: ✅ All data accurate

---

### Test 11: PDF Filename Format
**Steps**:
1. Export PDF on August 5, 2026
2. Verify filename: `BugReport_2026-08-05.pdf`
3. Export again same day
4. Verify same filename (overwrites or increments in browser)
5. Export on different day
6. Verify date updates in filename

**Expected Result**: ✅ Correct format: `BugReport_YYYY-MM-DD.pdf`

---

### Test 12: Loading Indicator
**Steps**:
1. Click "Export to PDF"
2. Select export scope
3. Click "Export"
4. Verify loading indicator appears:
   - Spinner animation visible
   - Text: "Generating PDF Report..."
5. Wait for download to complete
6. Verify loading indicator disappears
7. Verify success message appears (if implemented)

**Expected Result**: ✅ Loading state shows

---

### Test 13: Browser Compatibility
**Test in Multiple Browsers**:
- ✅ Chrome/Chromium
- ✅ Firefox
- ✅ Safari
- ✅ Edge

**Steps** (for each browser):
1. Login
2. Navigate to bugs page
3. Click "Export to PDF"
4. Verify modal displays correctly
5. Export and verify PDF downloads
6. Open PDF and verify content

**Expected Result**: ✅ Works in all modern browsers

---

### Test 14: Responsive Design
**Steps**:
1. Open bugs page on desktop
2. Verify "Export to PDF" button styled correctly
3. Resize browser to mobile width (375px)
4. Verify button still visible and functional
5. Click "Export to PDF"
6. Verify modal displays properly on mobile
7. Verify options readable on mobile
8. Complete export on mobile

**Expected Result**: ✅ Responsive design works

---

### Test 15: Error Handling
**Steps**:
1. Simulate error by disconnecting network
2. Click "Export to PDF"
3. Select options
4. Click "Export" (while offline)
5. Verify error message: "Failed to export PDF. Please try again."
6. Reconnect network
7. Try again
8. Verify works after reconnect

**Expected Result**: ✅ Error handling graceful

---

## Verification Checklist

| Test | Status | Notes |
|------|--------|-------|
| Button appears on bugs list | ⬜ | |
| Modal opens on click | ⬜ | |
| Current page export works | ⬜ | |
| All results export works | ⬜ | |
| Filters applied to export | ⬜ | |
| Search applied to export | ⬜ | |
| Large export warning shown | ⬜ | |
| Empty results handled | ⬜ | |
| Authentication required | ⬜ | |
| All user roles can export | ⬜ | |
| Modal close buttons work | ⬜ | |
| PDF content accurate | ⬜ | |
| Filename format correct | ⬜ | |
| Loading indicator shows | ⬜ | |
| Works in Chrome | ⬜ | |
| Works in Firefox | ⬜ | |
| Works in Safari | ⬜ | |
| Works in Edge | ⬜ | |
| Mobile responsive | ⬜ | |
| Error handling works | ⬜ | |

---

## Debugging Tips

### Check Browser Console
```javascript
// Open DevTools Console (F12) to see:
// 1. JavaScript errors
// 2. Network requests
// 3. Response status codes

// Check fetch request
console.log('Export data:', window.bugsFilterData);
```

### Check Server Logs
```bash
# For Docker
docker-compose logs web

# For local Flask
# Errors printed in terminal running `flask run`
```

### Check PDF Generation Issues
1. Verify ReportLab installed:
   ```bash
   python -c "from reportlab.lib.pagesizes import A4; print('OK')"
   ```

2. Check file permissions:
   ```bash
   ls -la app/utils/pdf_generator.py
   ```

3. Test PDF generation directly:
   ```python
   from app.utils.pdf_generator import BugReportGenerator
   from app.models import Bug
   bugs = Bug.query.limit(5).all()
   gen = BugReportGenerator(bugs=bugs)
   pdf = gen.generate_pdf()
   print(f"PDF size: {len(pdf)} bytes")
   ```

---

## Known Limitations & Notes

1. **Max Export**: Limited to 500 bugs per export (configurable in `config.py`)
2. **PDF Size**: Large exports (>400 bugs) may take 5-10 seconds
3. **Browser Download**: Download behavior depends on browser settings
4. **Date Format**: Uses UTC timezone for report generation time
5. **Comments/Attachments**: Only shows counts, not full content in PDF
6. **Page Breaks**: Automatic after 20 bugs per printed page

---

## Success Criteria

All tests should pass with:
- ✅ No Python errors in logs
- ✅ No JavaScript errors in browser console
- ✅ PDF downloads successfully
- ✅ PDF opens in PDF viewers
- ✅ PDF content is accurate
- ✅ Performance is acceptable (<30 seconds)

---

**Testing Date**: _______________
**Tester Name**: _______________
**Notes**: _______________

---

If all tests pass, the feature is ready for production deployment!
