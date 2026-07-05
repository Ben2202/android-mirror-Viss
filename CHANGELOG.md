# Changelog

## Unreleased

### Added
- Added a Stop Sync button to the main action row.
- Added an English changelog.
- Added `customtkinter` to the project requirements.

### Changed
- Reworked the action buttons so they appear in one equal-width row.
- Reworked detected devices into equal-size cards laid out side by side.
- Reused persistent input injectors per follower device instead of opening a new ADB shell for every event.
- Improved touch sync shutdown by stopping the active `getevent` listener and closing injectors.
- Expanded touch event parsing to include pressure, touch size, and orientation events.

### Fixed
- Prevented crashes when no master device or no followers are selected.
- Reset the master selector when no devices are detected.
- Improved handling for stopped or broken `su` sessions during event injection.
