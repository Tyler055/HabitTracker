# Habit Tracker Project

## By Jin, Niko, Tola, and Tyler

## Overview

Our Habit Tracker application helps users set, organize, and maintain goals across various timeframes—Daily, Weekly, Monthly, and Yearly. Progress is visually represented with percentage bars that update in real-time as goals are completed. To encourage consistency, the tracker includes motivational quotes and reminder notifications.

## Design

Users can add and name habits within categorized tabs. Each habit includes a checkbox that, when marked, updates the associated progress bar. Goals are grouped by category both in the interface and in the underlying codebase, ensuring a clean UI and maintainable structure.

The user interface supports intuitive navigation, allowing users to switch between different sections using a streamlined menu. The layout guides users directly to their desired content or functionality.

## Diagram

*(Insert a wireframe or flowchart here showing the relationship between tabs, goals, progress bars, and the notification system.)*

## Examples

*(Optional: Add screenshots of the UI, code snippets showing how goals are saved or loaded, or a step-by-step user interaction flow.)*


## Current Status (Final Developer Notes)

“I’ve fixed all the major implementation bugs—habits can now be added to any category on any page, and they save correctly in their respective categories. Everything appears to be working as intended, with no obvious issues remaining.

One edge-case bug remains unresolved. I understand what’s happening, but I’m not sure how to fix it cleanly from a structural standpoint. It only arises under specific conditions and would likely disappear with a different layout or architecture.

There are two flaws I’m aware of:

1. One I don't fully understand how to resolve logically.
2. The other I have an idea for, but didn’t have time to implement—it would require a significant structural rewrite.

That said, the rest of the system works well. Motivational quotes are included, and while you can technically add a notification with a time, it currently has no behavior beyond existing.
The “Advanced” page is the one area that still needs real attention. I didn’t do much with it, but the underlying features mostly exist—it just needs proper specialization and data display (right now, it shows `undefined`).

My full codebase is available on GitHub, to the best of my knowledge.”
— *Tyler*
