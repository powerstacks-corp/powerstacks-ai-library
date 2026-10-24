# Error Codes (Reference)

Status: Preview 0.11.0. Used by area A5.

## Sources and Attribution

Each row cites its source. All sources are by Microsoft Corporation and licensed under Creative Commons Attribution 4.0 International (CC BY 4.0), https://creativecommons.org/licenses/by/4.0/. Retrieved 2026-10-15. Changes: tables merged and reformatted, links and formatting reduced to text, exact duplicate rows removed, decimal values calculated from hex codes (and hex codes calculated from Windows error numbers for S3).

- S1: "App installation error codes for Microsoft Intune", https://learn.microsoft.com/troubleshoot/mem/intune/app-management/app-install-error-codes
- S2: "Common error codes and descriptions in Microsoft Intune", https://learn.microsoft.com/troubleshoot/mem/intune/general/troubleshoot-company-resource-access-problems
- S3: "MsiExec.exe and InstMsi.exe error messages", https://learn.microsoft.com/windows/win32/msi/error-codes
- S4: "Troubleshooting packaging, deployment, and query of Windows apps", https://learn.microsoft.com/windows/win32/appxpkg/troubleshooting

## How to Use

- Look up a code by its hex form (case-insensitive). The model stores app error codes as signed decimals; convert with `hex(code & 0xFFFFFFFF)`.
- A code can appear more than once with different text for different platforms or sources. Use the row that fits the device platform and app type; otherwise give the closest row and say which platform or source it is documented for.
- 0x8007XXXX codes are Windows errors whose number is the last four hex digits (for example 0x80070643 is Windows error 1603). S3 rows list them in that form.
- Quote Microsoft's text as Microsoft's guidance and cite the row's source. Do not add fixes of your own.
- If a code is not in this table, say "No Microsoft description found for this code."

## Table

| Hex | Decimal | Code name or note | Platform or context | Error message | Microsoft description and guidance | Source |
| --- | --- | --- | --- | --- | --- | --- |
| 0xC7D14FB5 | -942583883 |  | Android | The app failed to install. | This error message is displayed when Intune cannot determine the root cause of the Android app installation error. No information was provided by Android during the failure. This error is returned when the APK download succeeded, but the app installation failed. This error may occur more commonly due to a bad APK file that cannot be installed onto the device. A possible cause can be when Google Play Protect blocks the install of the app due to security concerns. Another possible cause of this error is when a device does not support the app. For example, if the app requires API version 21+ and the device currently has API version 19. Intune returns this error for both DA and KNOX devices and although there may be a notification that users can click to retry, if there is an issue with the APK, it will never continue to fail. If the app is an available app, the notification can be dismissed. However, if the app is required, it cannot be dismissed. | S1 |
| 0xC7D14FBA | -942583878 |  | Android | The app installation was canceled because the installation (APK) file was deleted after download, but before installation. | The download of the APK succeeded, but before the user installed the app the file was removed from the device. This could happen if there was a large time difference between download and install. For example, the user canceled the original install, waited, and then clicked the notification to try again. This error message is returned this for only DA scenarios. KNOX scenarios can be done silently. We do present a notification to retry so the user can accept instead of cancel. If the app is an available app, the notification can be dismissed. However, if the app is required, it cannot be dismissed. | S1 |
| 0xC7D14FBB | -942583877 |  | Android | The app installation was canceled because the process was restarted during installation. | The device was rebooted during the APK installation process, resulting in a canceled installation. This error message is returned for both DA and KNOX devices. Intune presents a notification that users can click to retry. If the app is an available app, the notification can be dismissed. However, if the app is required, it cannot be dismissed. | S1 |
| 0x87D1041C | -2016345060 |  | Android | The application was not detected after installation completed successfully. | The user explicitly uninstalled the app. This error is not returned from the client. It is an error produced when the app was installed at one point, but then the user uninstalled it. This error should only occur for required applications. Users can uninstall non-required apps. This error can only happen in DA. KNOX blocks the uninstall of managed apps. The next sync will repost the notification on the device for the user to install. The user can ignore the notification. This error will continue to be reported until the user installs the app. | S1 |
| 0xC7D14FB2 | -942583886 |  | Android | The download failed because of an unknown error. | This error occurs when the download fails. This error can commonly occur due to Wi-Fi issues or slow connections. This error is returned for only DA scenarios. For KNOX scenarios, the user is not prompted to install, this can be done silently. Intune presents a notification that users can click to retry. If the app is an available app, the notification can be dismissed. However, if the app is required, it cannot be dismissed. | S1 |
| 0xC7D15078 | -942583688 |  | Android | The download failed because of an unknown error. The policy will be retried the next time the device syncs. | This error occurs when the download fails. This error can commonly occur due to Wi-Fi issues or slow connections. This error is returned for only DA scenarios. For KNOX scenarios, the user is not prompted to install, this can be done silently. | S1 |
| 0xC7D14FB1 | -942583887 |  | Android | The end user canceled the app installation. | The user explicitly uninstalled the app. This error is returned when the Android OS install activity was canceled by the user. The user pressed the cancel button when the OS install prompt was presented or clicked away from the prompt. This error is returned for only DA scenarios. For KNOX scenarios, the user is not prompted to install, this can be done silently. Intune presents a notification that users can click to retry. If the app is an available app, the notification can be dismissed. However, if the app is required, it cannot be dismissed. Ask the user not to cancel the install. | S1 |
| 0xC7D15015 | -942583787 |  | Android | The file download process was unexpectedly stopped. | The OS stopped the download process before it was complete. This error can occur when the device has low battery or the download is taking too long. This error is returned for only DA scenarios. For KNOX scenarios, the user is not prompted to install, this can be done silently. Intune presents a notification that users can click to retry. If the app is an available app, the notification can be dismissed. However, if the app is required, it cannot be dismissed. Ensure the device has a reliable network connection. | S1 |
| 0xC7D1507C | -942583684 |  | Android | The file download service was unexpectedly stopped. The policy will be retried the next time the device syncs. | The OS ended the download process before it was completed. This error can occur when the device has low battery or the download is taking too long. This error is returned for only DA scenarios. For KNOX scenarios, the user is not prompted to install, this can be done silently. Manually sync the device or wait for 24 hours and check the status. | S1 |
| 0xC7D14FB8 | -942583880 |  | Android | The app failed to uninstall. | This error is a generic uninstall failure. The OS did not specify why the app failed to uninstall. Some admin apps cannot simply be uninstalled. Check to ensure the app can be uninstalled manually and collect the Company Portal logs if the uninstall fails. | S1 |
| 0xC7D14FB7 | -942583881 |  | Android | The app installation APK file used for the upgrade does not match the signature for the current app on the device. | Android OS has the limitation of requiring the signing cert for the upgrade version to be exactly the same as the cert used to sign the existing version. If the developer cannot use the same cert to sign the new version, you will need to uninstall the existing app and re-deploy the new app rather than upgrade the existing app. | S1 |
| 0xC7D14FB9 | -942583879 |  | Android | The end user canceled the app installation. | Educate the user to accept the Intune deployed app and install the app when prompted. | S1 |
| 0xC7D14FBC | -942583876 |  | Android | Uninstall of the app was canceled because the process was restarted during installation. | The app install process was terminated by the OS or the device was restarted. Retry the install and collect Company Portal logs if this error occurs again. | S1 |
| 0xC7D14FB6 | -942583882 |  | Android | The app installation APK file cannot be installed because it was not signed. | By default, Android OS requires apps to be signed. Ensure the app is signed before deployment. | S1 |
| 0xC7D14FB9 | -942583879 |  | Android | The end user canceled the app installation. (At the accept prompt) | Educate the user to accept the Intune deployed app and install the app when prompted. | S1 |
| 0x87D12906 | -2016335610 |  | iOS/iPadOS | Apple MDM Agent error: App installation command failed with no error reason specified. Retry app installation. | Apple MDM Agent returned that the installation command failed. | S1 |
| 0x87D1313C | -2016333508 |  | iOS/iPadOS | Network connection on the client was lost or interrupted. Later attempts should succeed in a better network environment. | The network connection was lost while the updated download service URL was sent to the device. Specifically, a server with the specified hostname could not be found. | S1 |
| 0x87D1313D | -2016333507 |  | iOS/iPadOS | Could not retrieve license for the app with iTunes Store ID | Sync the associated VPP token, then sync the device with Intune. If the issue persists, remove group assignment and reassign the VPP app as device-licensed. If the issue still persists, revoke the app license from the device by navigating to Apps > iOS > *select VPP app* > App licenses > *select device*. Then, revoke license and try re-assigning the app to the user group or device group. If the issue still persists, revoke all VPP licenses for the device by going to Devices > iOS > *select device* > Overview > Revoke licenses, then retire the device and re-enroll to Intune. | S1 |
| 0x87D11388 | -2016341112 |  | iOS/iPadOS | iOS/iPadOS device is currently busy. | The iOS/iPadOS device was busy, which resulted in an error. The device was locked. The user needs to unlock the device to install the app. | S1 |
| 0x87D13BA9 | -2016330839 | Source decimal: -2016345112 | iOS/iPadOS | The app installation has failed. (ErrorUserEnrollmentUnsupported) | The VPP app is deployed with the Device licensing type but only the User licensing type is supported for BYOD (bring your own device) devices enrolled with account driven Apple User Enrollment. Change the licensing type for the assignments or create a separate assignment for the users. | S1 |
| 0x87D13B64 | -2016330908 |  | iOS/iPadOS | The app installation has failed. | An app installation failure occurred. iOS/iPadOS Console logs are needed to troubleshoot this error. | S1 |
| 0x87D13B66 | -2016330906 |  | iOS/iPadOS | The app is managed, but has expired or been removed by the user. | Either the user explicitly uninstalled the app, or the app is expired but failed to download, or the app detection does not match the response from the device. Additionally, this error could occur based on an iOS/iPadOS 9.2.2 platform bug. | S1 |
| 0x87D13B60 | -2016330912 |  | iOS/iPadOS | The app is scheduled for installation, but needs a redemption code to complete the transaction. | This error typically occurs with iOS Store apps which are paid apps. | S1 |
| 0x87D13B7D | -2016330883 |  | iOS/iPadOS | Unknown error. | An unknown app installation error occurred. This error code can be returned for multiple reasons, one of which is an expired VPP token in Intune. As a general recommendation, whenever an unknown error is encountered, ensure that the Volume Purchase Program (VPP) token is checked to verify that it's current and functional. | S1 |
| 0x87D1041C | -2016345060 |  | iOS/iPadOS | The application was not detected after installation completed successfully. | The app detection process did not match with the response from the device. | S1 |
| 0x87D13B62 | -2016330910 |  | iOS/iPadOS | The user rejected the offer to install the app. | During initial app install, the user clicked cancel. Ask the user to accept the install request the next time. | S1 |
| 0x87D13B63 | -2016330909 |  | iOS/iPadOS | The user rejected the offer to update the app. | The end user clicked cancel during the update process. Deploy as required or educate the user to accept the upgrade prompt. | S1 |
| 0x87D103E8 | -2016345112 |  | iOS/iPadOS | Unknown error | An unknown app installation error occurred. This is the resulting error when other errors have not occurred. | S1 |
| 0x87D13B93 | -2016330861 |  | iOS/iPadOS | Can only install VPP apps on Shared iPad. | The apps must be obtained using Apple Volume Purchase Program to install on a Shared iPad. | S1 |
| 0x87D13B94 | -2016330860 |  | iOS/iPadOS | Can't install apps when App Store is disabled. | The App Store must be enabled for the user to install the app. | S1 |
| 0x87D13B95 | -2016330859 |  | iOS/iPadOS | Can't find VPP license for app. | Try revoking and reassigning the app license. | S1 |
| 0x87D13B96 | -2016330858 |  | iOS/iPadOS | Can't install system apps with your MDM provider. | Installing apps that are pre-installed by the iOS/iPadOS operating system is not a supported scenario. | S1 |
| 0x87D13B97 | -2016330857 |  | iOS/iPadOS | Can't install apps when device is in Lost Mode. | All use of the device is blocked in Lost Mode. Disable Lost Mode to install apps. | S1 |
| 0x87D13B98 | -2016330856 |  | iOS/iPadOS | Can't install apps when device is in kiosk mode. | Try adding this device to an exclude group for kiosk mode configuration policy to install apps. | S1 |
| 0x87D13B9C | -2016330852 |  | iOS/iPadOS | Can't install 32-bit apps on this device. | The device doesn't support installing 32-bit apps. Try deploying the 64-bit version of the app. | S1 |
| 0x87D13B99 | -2016330855 |  | iOS/iPadOS | User must sign in to the App Store. | The user needs to sign in to the App Store before the app can be installed. | S1 |
| 0x87D13B9A | -2016330854 |  | iOS/iPadOS | Unknown problem. Please try again. | The app installation failed due to an unknown reason. Try again later. | S1 |
| 0x87D13B9B | -2016330853 |  | iOS/iPadOS | The app installation failed. Intune will try again the next time the device syncs. | The app installation encountered a device error. Sync the device to try installing the app again. | S1 |
| 0x87D13B7E | -2016330882 |  | iOS/iPadOS | License Assignment failed with Apple error 'No VPP licenses remaining' | This behavior is by design. To resolve this, purchase additional VPP licenses or reclaim licenses from users no longer targeted. | S1 |
| 0x87D13B6E | -2016330898 |  | iOS/iPadOS | App Install Failure 12024: Unknown cause. | Apple hasn't given us sufficient information to determine why the install failed. Nothing to report. | S1 |
| 0x87D13B7F | -2016330881 |  | iOS/iPadOS | Needed app configuration policy not present, ensure policy is targeted to same groups. | App requires app config but no app config is targeted. Admin should make sure the groups the app is targeted to also has the required app config targeted to the groups. | S1 |
| 0x87D13B69 | -2016330903 |  | iOS/iPadOS | Device VPP licensing is only applicable for iOS/iPadOS 9.0+ devices. | Upgrade affected iOS/iPadOS devices to iOS/iPadOS 9.0+. | S1 |
| 0x87D13B8F | -2016330865 |  | iOS/iPadOS | The application is installed on the device but is unmanaged. | This error only happens to LOB apps. The app was installed outside of Intune. To address this error, uninstall the app from the device. The next time the device sync happens, the device should install the app from Intune. | S1 |
| 0x87D13B68 | -2016330904 |  | iOS/iPadOS | User declined app management | Ask the user to accept app management. | S1 |
| 0x87D1279D | -2016335971 |  | iOS/iPadOS | Unknown error. | This error happens to iOS store apps, but the error scenario is unknown. | S1 |
| 0x87D13B9D | -2016330851 |  | iOS/iPadOS | The latest version of the app failed to update from an earlier version. | This error message is displayed if the app is installed and managed but with the incorrect version on the device. This situation includes when a device has received a command to update an app but the new version has not yet been installed and reported back. This error will be reported for the first check-in of a device after the upgrade has been deployed, and will occur until the device reports that the new version is installed, or fails due to a different error. | S1 |
| 0x87D13B6F | -2016330897 |  | iOS/iPadOS | Your connection to Intune timed out. | App Manifest validation failure due to network connectivity(timeout) | S1 |
| 0x87D13B70 | -2016330896 |  | iOS/iPadOS | You lost connection to the Internet. | App Manifest validation failure due to network connectivity(Cannot Find Host) | S1 |
| 0x87D13B72 | -2016330894 |  | iOS/iPadOS | You lost connection to the Internet. | App Manifest validation failure due to network connectivity(Connection Lost) | S1 |
| 0x87D13B73 | -2016330893 |  | iOS/iPadOS | You lost connection to the Internet. | App Manifest validation failure due to network connectivity(Not Connected to internet) | S1 |
| 0x87D13B77 | -2016330889 |  | iOS/iPadOS | The secure connection failed. | App Manifest validation failure due to network connectivity(Secure Connection Failed) | S1 |
| 0x87D13B80 | -2016330880 |  | iOS/iPadOS | CannotConnectToITunesStoreError | App install failed due to failure to Connect To ITunes Store | S1 |
| 0x87D13B9F | -2016330849 |  | iOS/iPadOS | The VPP App has an update available | This code is returned when a VPP app is installed but there is a newer version available. | S1 |
| 0x87D13B9E | -2016330850 | Source decimal: 2016330850 | iOS/iPadOS | Can't enforce app uninstall setting. Retry installing the app. | The app is already installed on the device but the "uninstall on retire" setting does not match the configured value. Advise the user to request the app-install from Company Portal to attempt applying the "uninstall on retire" setting again. | S1 |
| 0x80073CFF | -2147009281 |  | Windows and other | (client error) | To install this app, you must have a sideloading-enabled system. Make sure that the app package is signed with a trusted signature and installed on a domain-joined device that has the AllowAllTrustedApps policy enabled, or a device that has a Windows Sideloading license with the AllowAllTrustedApps policy enabled. For more information, see Troubleshooting packaging, deployment, and query of Windows Store apps. | S1 |
| 0x80CF201C | -2133909476 |  | Windows and other | (client error) | To install this app, you must have a sideloading-enabled system. Make sure that the app package is signed with a trusted signature and installed on a domain-joined device that has the AllowAllTrustedApps policy enabled, or a device that has a Windows Sideloading license with the AllowAllTrustedApps policy enabled. For more information, see Troubleshooting packaging, deployment, and query of Windows Store apps. | S1 |
| 0x80073CF0 | -2147009296 |  | Windows and other | The package is unsigned. The publisher name does not match the signing certificate subject. Check the AppxPackagingOM event log for information. For more information, see Troubleshooting packaging, deployment, and query of Windows Store apps. | The package could not be opened. | S1 |
| 0x80073CF3 | -2147009293 | Source decimal: -2147009296 | Windows and other | The incoming package conflicts with an installed package. A specified package dependency is not found. The package does not support the correct processor architecture. Check the AppXDeployment-Server event log for information. For more information, see Troubleshooting packaging, deployment, and query of Windows Store apps. | The package failed update, dependency, or conflict validation. | S1 |
| 0x80073CFB | -2147009285 |  | Windows and other | Increment the version number of the app, then rebuild and re-sign the package. Remove the old package for every user on the system before you install the new package. For more information, see Troubleshooting packaging, deployment, and query of Windows Store apps. | The provided package is already installed, and reinstallation of the package is blocked. You could receive this error if you are installing a package that is not identical to the package that is already installed. Confirm the digital signature is also part of the package. When a package is rebuilt or re-signed, that package is no longer bitwise identical to the previously installed package. Two possible options to fix this error are as follows: | S1 |
| 0x87D1041C | -2016345060 |  | Windows and other | The end user uninstalled the app. The identity information in the package does not match what device reports for bad apps. For self-updating MSIs, the product version does not match the information of the app after it is updated outside of Intune. Instruct the user to reinstall the app from the company portal. Note that required apps will be reinstalled automatically when the device next checks in. | Application installation succeeded but application is not detected. The app was deployed successfully by Intune, then subsequently uninstalled. Reasons for the app being uninstalled include: | S1 |
| 0x8000FFFF | -2147418113 |  | Windows and other |  | An unexpected error occurred during installation. Check the installation logs for additional information. | S1 |
|  |  | Status 10 (APP_CI_ENFORCEMENT_IN_PROGRESS) | Windows MDM app status | Installation in progress |  | S2 |
|  |  | Status 20 (APP_CI_ENFORCEMENT_IN_PROGRESS_WAITING_CONTENT) | Windows MDM app status | Waiting for content |  | S2 |
|  |  | Status 30 (APP_CI_ENFORCEMENT_ERROR_RETRIEVING_CONTENT) | Windows MDM app status | Retrieving content | Probable Cause: Job status 30 indicates that a user download of an app failed. Likely causes for this may be: The device lost Internet connectivity while the download was in progress. The certificate issued to the device at the time of enrollment may have expired. Mitigation: Launch the Company Apps app from Control Panel on the device to confirm that the device certificate hasn't expired; if it has then you will need to re-enroll the device. Confirm that the device is connected to the Internet and try to request the app again. | S2 |
|  |  | Status 40 (APP_CI_ENFORCEMENT_IN_PROGRESS_CONTENT_DOWNLOADED) | Windows MDM app status | Content download complete |  | S2 |
|  |  | Status 50 (APP_CI_ENFORCEMENT_IN_PROGRESS_INSTALLING) | Windows MDM app status | Installation in progress |  | S2 |
|  |  | Status 60 (APP_CI_ENFORCEMENT_ERROR_INSTALLING) | Windows MDM app status | Installation Error occurred | The app installation failed after download. The code signing certificate with which app was signed is not present on the device. A framework dependency on which the application depends is not found installed on the device. Ensure that the code signing certificate with which your app was signed is present on the device and confirm with the admin that such a certificate was targeted for all enterprise enrolled Windows RT devices. In case the installation failure is due to a missing framework dependency, the admin will have to re-publish the application again packaging the framework along with the application package. The application package downloaded isn't a valid package, may have been corrupted, or may not be compatible with the OS version on the device. | S2 |
|  |  | Status 70 (APP_CI_ENFORCEMENT_SUCCEEDED) | Windows MDM app status | Installation Success |  | S2 |
|  |  | Status 80 (APP_CI_ENFORCEMENT_IN_PROGRESS) | Windows MDM app status | Uninstall in progress |  | S2 |
|  |  | Status 90 (APP_CI_ENFORCEMENT_ERROR) | Windows MDM app status | Uninstall Error occurred |  | S2 |
|  |  | Status 100 (APP_CI_ENFORCEMENT_SUCCEEDED) | Windows MDM app status | Uninstall Success |  | S2 |
|  |  | Status 110 (APP_CI_ENFORCEMENT_ERROR) | Windows MDM app status | Content hash mismatch |  | S2 |
|  |  | Status 120 (APP_CI_ENFORCEMENT_ERROR) | Windows MDM app status | SLK / side loading not enabled |  | S2 |
|  |  | Status 130 (APP_CI_ENFORCEMENT_ERROR) | Windows MDM app status | MSADP license install failed |  | S2 |
|  |  | Status No status (APP_CI_ENFORCEMENT_UNKNOWN) | Windows MDM app status | n/a | The status is currently unknown. | S2 |
| 0x87D1FDF3 | -2016281101 |  | Company resource access (common errors) | MDM CRP request not found |  | S2 |
| 0x87D1FDF2 | -2016281102 |  | Company resource access (common errors) | NDES URL not found |  | S2 |
| 0x87D1FDF1 | -2016281103 |  | Company resource access (common errors) | MDM CRP certificate info not found |  | S2 |
| 0x87D1FDF0 | -2016281104 |  | Company resource access (common errors) | MDM CI certificate info not found |  | S2 |
| 0x87D1FDEF | -2016281105 |  | Company resource access (common errors) | Failed to evaluate the Rule |  | S2 |
| 0x87D1FDEE | -2016281106 |  | Company resource access (common errors) | Not applicable because it lost in conflict resolution |  | S2 |
| 0x87D1FDED | -2016281107 |  | Company resource access (common errors) | Unsupported setting discovery source |  | S2 |
| 0x87D1FDEC | -2016281108 |  | Company resource access (common errors) | Referenced setting not found in CI |  | S2 |
| 0x87D1FDEB | -2016281109 |  | Company resource access (common errors) | Data type conversion failed |  | S2 |
| 0x87D1FDEA | -2016281110 |  | Company resource access (common errors) | Invalid parameter to CIM setting |  | S2 |
| 0x87D1FDE9 | -2016281111 |  | Company resource access (common errors) | Not applicable for this device |  | S2 |
| 0x87D1FDE8 | -2016281112 |  | Company resource access (common errors) | Remediation failed |  | S2 |
| 0x87D13B67 | -2016330905 |  | Company resource access (common errors) | The app state is unknown |  | S2 |
| 0x87D13B66 | -2016330906 |  | Company resource access (common errors) | The app is managed, but has been removed by the user |  | S2 |
| 0x87D13B65 | -2016330907 |  | Company resource access (common errors) | The device is redeeming the redemption code |  | S2 |
| 0x87D13B64 | -2016330908 |  | Company resource access (common errors) | The app install has failed |  | S2 |
| 0x87D13B63 | -2016330909 |  | Company resource access (common errors) | The user rejected the offer to update the app |  | S2 |
| 0x87D13B62 | -2016330910 |  | Company resource access (common errors) | The user rejected the offer to install the app |  | S2 |
| 0x87D13B61 | -2016330911 |  | Company resource access (common errors) | The user has installed the app before managed app installation could take place |  | S2 |
| 0x87D13B60 | -2016330912 |  | Company resource access (common errors) | The app is scheduled for installation, but needs a redemption code to complete the transaction |  | S2 |
| 0x87D1138B | -2016341109 |  | Company resource access (common errors) | iOS device has returned an error |  | S2 |
| 0x87D1138A | -2016341110 |  | Company resource access (common errors) | iOS device has rejected the command due to incorrect format |  | S2 |
| 0x87D11389 | -2016341111 |  | Company resource access (common errors) | iOS device has returned an unexpected Idle status |  | S2 |
| 0x87D11388 | -2016341112 |  | Company resource access (common errors) | iOS device is currently busy |  | S2 |
| 0x87D1B799 | -2016299111 |  | Service errors | Internal error |  | S2 |
| 0x87D1B798 | -2016299112 |  | Service errors | Internal error |  | S2 |
| 0x87D1B3B1 | -2016300111 |  | Service errors | 36001:(internal error) |  | S2 |
| 0x87D1B3B0 | -2016300112 |  | Service errors | 36000:Cellular already configured |  | S2 |
| 0x87D1AFCA | -2016301110 |  | Service errors | 35002:Multiple fonts in a single payload |  | S2 |
| 0x87D1AFC9 | -2016301111 |  | Service errors | 35001:Failed font installation |  | S2 |
| 0x87D1AFC8 | -2016301112 |  | Service errors | 35000:Invalid font data |  | S2 |
| 0x87D1ABE3 | -2016302109 |  | Service errors | 34003:Kerberos principal name invalid |  | S2 |
| 0x87D1ABE2 | -2016302110 |  | Service errors | 34002:Kerberos principal name missing |  | S2 |
| 0x87D1ABE1 | -2016302111 |  | Service errors | 34001:Invalid URL match pattern |  | S2 |
| 0x87D1ABE0 | -2016302112 |  | Service errors | 34000:Invalid app identifier match pattern |  | S2 |
| 0x87D1A410 | -2016304112 |  | Service errors | 32000:Too many apps |  | S2 |
| 0x87D1A029 | -2016305111 |  | Service errors | 31001:Cannot apply settings |  | S2 |
| 0x87D1A028 | -2016305112 |  | Service errors | 31000:Cannot apply credential |  | S2 |
| 0x87D19C41 | -2016306111 |  | Service errors | 30001:Timed out |  | S2 |
| 0x87D19C40 | -2016306112 |  | Service errors | 30000:Authentication failed |  | S2 |
| 0x87D1985B | -2016307109 |  | Service errors | 29003:Bad certificate data |  | S2 |
| 0x87D1985A | -2016307110 |  | Service errors | 29002: |  | S2 |
| 0x87D19859 | -2016307111 |  | Service errors | 29001: |  | S2 |
| 0x87D19858 | -2016307112 |  | Service errors | 29000:Device not supervised |  | S2 |
| 0x87D19472 | -2016308110 |  | Service errors | 28002:Cannot set wallpaper |  | S2 |
| 0x87D19471 | -2016308111 |  | Service errors | 28001:Bad wallpaper image |  | S2 |
| 0x87D19470 | -2016308112 |  | Service errors | 28000:Unknown item |  | S2 |
| 0x87D18CA1 | -2016310111 |  | Service errors | 26001:File level encryption unsupported |  | S2 |
| 0x87D18CA0 | -2016310112 |  | Service errors | 26000:Block level encryption unsupported |  | S2 |
| 0x87D188BA | -2016311110 |  | Service errors | 25002:Cannot remove |  | S2 |
| 0x87D188B9 | -2016311111 |  | Service errors | 25001:Cannot install |  | S2 |
| 0x87D188B8 | -2016311112 |  | Service errors | 25000:Bad profile |  | S2 |
| 0x87D184D3 | -2016312109 |  | Service errors | 24003:Bad final profile |  | S2 |
| 0x87D184D2 | -2016312110 |  | Service errors | 24002:Bad identity payload |  | S2 |
| 0x87D184D1 | -2016312111 |  | Service errors | 24001:Cannot sign attribute dictionary |  | S2 |
| 0x87D184D0 | -2016312112 |  | Service errors | 24000:Cannot create attribute dictionary |  | S2 |
| 0x87D180EA | -2016313110 |  | Service errors | 23002:Invalid server certificate |  | S2 |
| 0x87D180E9 | -2016313111 |  | Service errors | 23001:Bad server response |  | S2 |
| 0x87D180E8 | -2016313112 |  | Service errors | 23000:Bad identity |  | S2 |
| 0x87D17D0D | -2016314099 |  | Service errors | 22013:Invalid PKIOperation response |  | S2 |
| 0x87D17D0C | -2016314100 |  | Service errors | 22012:Cannot store CACertificate |  | S2 |
| 0x87D17D0B | -2016314101 |  | Service errors | 22011:Cannot generate CSR |  | S2 |
| 0x87D17D0A | -2016314102 |  | Service errors | 22010:Cannot store temporary identity |  | S2 |
| 0x87D17D09 | -2016314103 |  | Service errors | 22009:Cannot create temporary identity |  | S2 |
| 0x87D17D08 | -2016314104 |  | Service errors | 22008:Cannot create identity |  | S2 |
| 0x87D17D07 | -2016314105 |  | Service errors | 22007:Invalid signed certificate |  | S2 |
| 0x87D17D06 | -2016314106 |  | Service errors | 22006:Insufficient CACaps |  | S2 |
| 0x87D17D05 | -2016314107 |  | Service errors | 22005:Network error |  | S2 |
| 0x87D17D04 | -2016314108 |  | Service errors | 22004:Unsupported certificate configuration |  | S2 |
| 0x87D17D03 | -2016314109 |  | Service errors | 22003:Invalid RAResponse |  | S2 |
| 0x87D17D02 | -2016314110 |  | Service errors | 22002:Invalid CAResponse |  | S2 |
| 0x87D17D01 | -2016314111 |  | Service errors | 22001:Cannot generate key pair |  | S2 |
| 0x87D17D00 | -2016314112 |  | Service errors | 22000:Invalid key usage |  | S2 |
| 0x87D1791F | -2016315105 |  | Service errors | 21007:Cannot verify account |  | S2 |
| 0x87D1791E | -2016315106 |  | Service errors | 21006:Cannot decrypt certificate |  | S2 |
| 0x87D1791D | -2016315107 |  | Service errors | 21005:Account not unique (Email Profile already exists on device) |  | S2 |
| 0x87D1791C | -2016315108 |  | Service errors | 21004:Cannot create account |  | S2 |
| 0x87D1791B | -2016315109 |  | Service errors | 21003:No host name |  | S2 |
| 0x87D1791A | -2016315110 |  | Service errors | 21002:Cannot comply with encryption policy from server |  | S2 |
| 0x87D17919 | -2016315111 |  | Service errors | 21001:Cannot comply with policy from server |  | S2 |
| 0x87D17918 | -2016315112 |  | Service errors | 21000:Cannot get policy from server |  | S2 |
| 0x87D17532 | -2016316110 |  | Service errors | 20002:Account not unique |  | S2 |
| 0x87D17531 | -2016316111 |  | Service errors | 20001:No host name |  | S2 |
| 0x87D17530 | -2016316112 |  | Service errors | 20000:Cannot create account |  | S2 |
| 0x87D1714A | -2016317110 |  | Service errors | 19002:Account not unique |  | S2 |
| 0x87D17149 | -2016317111 |  | Service errors | 19001:No host name |  | S2 |
| 0x87D17148 | -2016317112 |  | Service errors | 19000:Cannot create account |  | S2 |
| 0x87D16D62 | -2016318110 |  | Service errors | 18002:Invalid credentials |  | S2 |
| 0x87D16D61 | -2016318111 |  | Service errors | 18001:Host unreachable |  | S2 |
| 0x87D16D60 | -2016318112 |  | Service errors | 18000:Unknown error |  | S2 |
| 0x87D1697A | -2016319110 |  | Service errors | 17002:Account not unique |  | S2 |
| 0x87D16979 | -2016319111 |  | Service errors | 17001:No host name |  | S2 |
| 0x87D16978 | -2016319112 |  | Service errors | 17000:Cannot create account |  | S2 |
| 0x87D16592 | -2016320110 |  | Service errors | 16002:Account not unique |  | S2 |
| 0x87D16591 | -2016320111 |  | Service errors | 16001:No host name |  | S2 |
| 0x87D16590 | -2016320112 |  | Service errors | 16000:Cannot create subscription |  | S2 |
| 0x87D161AB | -2016321109 |  | Service errors | 15003:Invalid certificate |  | S2 |
| 0x87D161AA | -2016321110 |  | Service errors | 15002:Cannot lock network configuration |  | S2 |
| 0x87D161A9 | -2016321111 |  | Service errors | 15001:Cannot remove VPN |  | S2 |
| 0x87D161A8 | -2016321112 |  | Service errors | 15000:Cannot install VPN |  | S2 |
| 0x87D15DC2 | -2016322110 |  | Service errors | 14002:Cloud configuration already exists |  | S2 |
| 0x87D15DC1 | -2016322111 |  | Service errors | 14001:Device locked |  | S2 |
| 0x87D15DC0 | -2016322112 |  | Service errors | 14000:Invalid field |  | S2 |
| 0x87D159DD | -2016323107 |  | Service errors | 13005:Cannot set up proxy |  | S2 |
| 0x87D159DC | -2016323108 |  | Service errors | 13004:Cannot set up EAP |  | S2 |
| 0x87D159DB | -2016323109 |  | Service errors | 13003:Cannot create WiFi configuration |  | S2 |
| 0x87D159DA | -2016323110 |  | Service errors | 13002:Password required |  | S2 |
| 0x87D159D9 | -2016323111 |  | Service errors | 13001:Username required |  | S2 |
| 0x87D159D8 | -2016323112 |  | Service errors | 13000:Cannot install |  | S2 |
| 0x87D1561A | -2016324070 |  | Service errors | 12042:Unknown locale code |  | S2 |
| 0x87D15619 | -2016324071 |  | Service errors | 12041:Unknown language code |  | S2 |
| 0x87D15618 | -2016324072 |  | Service errors | 12040:iTunes store login required |  | S2 |
| 0x87D15617 | -2016324073 |  | Service errors | 12039:(unused) |  | S2 |
| 0x87D15616 | -2016324074 |  | Service errors | 12038:App not managed |  | S2 |
| 0x87D15615 | -2016324075 |  | Service errors | 12037:Invalid redemption code |  | S2 |
| 0x87D15614 | -2016324076 |  | Service errors | 12036:Cannot remove app in current state |  | S2 |
| 0x87D15613 | -2016324077 |  | Service errors | 12035:App cannot be purchased |  | S2 |
| 0x87D15612 | -2016324078 |  | Service errors | 12034:URL is not HTTPS |  | S2 |
| 0x87D15611 | -2016324079 |  | Service errors | 12033:Invalid manifest |  | S2 |
| 0x87D15610 | -2016324080 |  | Service errors | 12032:Too many apps in manifest |  | S2 |
| 0x87D1560F | -2016324081 |  | Service errors | 12031:App installation disabled |  | S2 |
| 0x87D1560E | -2016324082 |  | Service errors | 12030:Invalid URL |  | S2 |
| 0x87D1560D | -2016324083 |  | Service errors | 12029:App not managed |  | S2 |
| 0x87D1560C | -2016324084 |  | Service errors | 12028:Not waiting for redemption |  | S2 |
| 0x87D1560B | -2016324085 |  | Service errors | 12027:Not an app |  | S2 |
| 0x87D1560A | -2016324086 |  | Service errors | 12026:App already queued |  | S2 |
| 0x87D15609 | -2016324087 |  | Service errors | 12025:App already installed |  | S2 |
| 0x87D15608 | -2016324088 |  | Service errors | 12024:Could not validate app manifest |  | S2 |
| 0x87D15607 | -2016324089 |  | Service errors | 12023:Could not validate app iD |  | S2 |
| 0x87D15606 | -2016324090 |  | Service errors | 12022:Invalid topic |  | S2 |
| 0x87D15605 | -2016324091 |  | Service errors | 12021:Invalid request type |  | S2 |
| 0x87D15604 | -2016324092 |  | Service errors | 12020:Unauthorized by server |  | S2 |
| 0x87D15603 | -2016324093 |  | Service errors | 12019:Cannot copy escrow secret |  | S2 |
| 0x87D15602 | -2016324094 |  | Service errors | 12018:Cannot copy escrow keybag data |  | S2 |
| 0x87D15601 | -2016324095 |  | Service errors | 12017:Cannot create escrow keybag |  | S2 |
| 0x87D15600 | -2016324096 |  | Service errors | 12016:Missing identity |  | S2 |
| 0x87D155FF | -2016324097 |  | Service errors | 12015:Cannot get push token |  | S2 |
| 0x87D155FE | -2016324098 |  | Service errors | 12014:Provisioning profile not managed |  | S2 |
| 0x87D155FD | -2016324099 |  | Service errors | 12013:Profile not managed |  | S2 |
| 0x87D155FC | -2016324100 |  | Service errors | 12012:MDM replacement mismatch |  | S2 |
| 0x87D155FB | -2016324101 |  | Service errors | 12011:Invalid MDM configuration |  | S2 |
| 0x87D155FA | -2016324102 |  | Service errors | 12010:Internal inconsistency error |  | S2 |
| 0x87D155F9 | -2016324103 |  | Service errors | 12009:Invalid replacement profile |  | S2 |
| 0x87D155F8 | -2016324104 |  | Service errors | 12008:Malformed request |  | S2 |
| 0x87D155F7 | -2016324105 |  | Service errors | 12007:Not authorized |  | S2 |
| 0x87D155F6 | -2016324106 |  | Service errors | 12006:Redirect refused |  | S2 |
| 0x87D155F5 | -2016324107 |  | Service errors | 12005:Cannot find certificate |  | S2 |
| 0x87D155F4 | -2016324108 |  | Service errors | 12004:Invalid push certificate |  | S2 |
| 0x87D155F3 | -2016324109 |  | Service errors | 12003:Invalid challenge response |  | S2 |
| 0x87D155F2 | -2016324110 |  | Service errors | 12002:Cannot check in |  | S2 |
| 0x87D155F1 | -2016324111 |  | Service errors | 12001:Multiple MDM instances |  | S2 |
| 0x87D155F0 | -2016324112 |  | Service errors | 12000:Invalid access rights |  | S2 |
| 0x87D15209 | -2016325111 |  | Service errors | 11001:Custom APN already installed |  | S2 |
| 0x87D15208 | -2016325112 |  | Service errors | 11000:Cannot install APN |  | S2 |
| 0x87D14E21 | -2016326111 |  | Service errors | 10001:Invalid signer |  | S2 |
| 0x87D14E20 | -2016326112 |  | Service errors | 10000:Cannot install defaults |  | S2 |
| 0x87D14A3E | -2016327106 |  | Service errors | 9006:Certificate is not an identity |  | S2 |
| 0x87D14A3D | -2016327107 |  | Service errors | 9005:Certificate is malformed |  | S2 |
| 0x87D14A3C | -2016327108 |  | Service errors | 9004:Cannot store root certificate |  | S2 |
| 0x87D14A3B | -2016327109 |  | Service errors | 9003:Cannot store WAPI data |  | S2 |
| 0x87D14A3A | -2016327110 |  | Service errors | 9002:Cannot store certificate |  | S2 |
| 0x87D14A39 | -2016327111 |  | Service errors | 9001:Too many certificates in a payload |  | S2 |
| 0x87D14A38 | -2016327112 |  | Service errors | 9000:Invalid password |  | S2 |
| 0x87D14650 | -2016328112 |  | Service errors | 8000:Cannot install Web Clip |  | S2 |
| 0x87D1426F | -2016329105 |  | Service errors | 7007:SMTP account is misconfigured |  | S2 |
| 0x87D1426E | -2016329106 |  | Service errors | 7006:POP account is misconfigured |  | S2 |
| 0x87D1426D | -2016329107 |  | Service errors | 7005:IMAP account is misconfigured |  | S2 |
| 0x87D1426C | -2016329108 |  | Service errors | 7004:SMIME certificate is bad |  | S2 |
| 0x87D1426B | -2016329109 |  | Service errors | 7003:SMIME certificate not found |  | S2 |
| 0x87D1426A | -2016329110 |  | Service errors | 7002:Unknown error occurred during validation |  | S2 |
| 0x87D14269 | -2016329111 |  | Service errors | 7001:Invalid credentials |  | S2 |
| 0x87D14268 | -2016329112 |  | Service errors | 7000:Host unreachable |  | S2 |
| 0x87D13E82 | -2016330110 |  | Service errors | 6002:Cannot create query |  | S2 |
| 0x87D13E81 | -2016330111 |  | Service errors | 6001:Empty string |  | S2 |
| 0x87D13E80 | -2016330112 |  | Service errors | 6000:Keychain system error |  | S2 |
| 0x87D13AA7 | -2016331097 |  | Service errors | 5015:Cannot set grace period |  | S2 |
| 0x87D13AA6 | -2016331098 |  | Service errors | 5014:Cannot set passcode |  | S2 |
| 0x87D13AA5 | -2016331099 |  | Service errors | 5013:Cannot clear passcode |  | S2 |
| 0x87D13AA4 | -2016331100 |  | Service errors | 5012:(unused) |  | S2 |
| 0x87D13AA4 | -2016331103 | Hex and status code differ in source (hex = -2016331100) | Service errors | 5009:(unused) |  | S2 |
| 0x87D13AA0 | -2016331104 |  | Service errors | 5008:Passcode too recent |  | S2 |
| 0x87D13A9F | -2016331105 |  | Service errors | 5007:Passcode expired |  | S2 |
| 0x87D13AA3 | -2016331106 | Hex and status code differ in source (hex = -2016331101) | Service errors | 5006:Passcode requires alpha characters |  | S2 |
| 0x87D13A9D | -2016331107 |  | Service errors | 5005:Passcode requires number |  | S2 |
| 0x87D13A9C | -2016331108 |  | Service errors | 5004:Passcode has ascending descending characters |  | S2 |
| 0x87D13A9B | -2016331109 |  | Service errors | 5003:Passcode has repeating characters |  | S2 |
| 0x87D13A9A | -2016331110 |  | Service errors | 5002:Too few complex characters |  | S2 |
| 0x87D13A99 | -2016331111 |  | Service errors | 5001:Too few unique characters |  | S2 |
| 0x87D13A98 | -2016331112 |  | Service errors | 5000:Passcode too short |  | S2 |
| 0x87D136C3 | -2016332093 |  | Service errors | 4019:Multiple App Lock payloads |  | S2 |
| 0x87D136C2 | -2016332094 |  | Service errors | 4018:Multiple APN or Cellular payloads |  | S2 |
| 0x87D136C1 | -2016332095 |  | Service errors | 4017:Multiple global HTTPProxy payloads |  | S2 |
| 0x87D136C0 | -2016332096 |  | Service errors | 4016:(Internal error) |  | S2 |
| 0x87D136BF | -2016332097 |  | Service errors | 4015:Replacement profile does not contain an MDM payload |  | S2 |
| 0x87D136BE | -2016332098 |  | Service errors | 4014:No device identity available |  | S2 |
| 0x87D136BD | -2016332099 |  | Service errors | 4013:Update failed |  | S2 |
| 0x87D136BC | -2016332100 |  | Service errors | 4012:Profile is not updatable |  | S2 |
| 0x87D136BB | -2016332101 |  | Service errors | 4011:Final profile is not a configuration profile |  | S2 |
| 0x87D136BA | -2016332102 |  | Service errors | 4010:Updated profile does not have the same identifier |  | S2 |
| 0x87D136B9 | -2016332103 |  | Service errors | 4009:Device locked |  | S2 |
| 0x87D136B8 | -2016332104 |  | Service errors | 4008:Mismatched certificates |  | S2 |
| 0x87D136B7 | -2016332105 |  | Service errors | 4007:Unrecognized file format |  | S2 |
| 0x87D136B6 | -2016332106 |  | Service errors | 4006:Profile removal date is in the past |  | S2 |
| 0x87D136B5 | -2016332107 |  | Service errors | 4005:Passcode does not comply |  | S2 |
| 0x87D136B4 | -2016332108 |  | Service errors | 4004:User canceled installation |  | S2 |
| 0x87D136B3 | -2016332109 |  | Service errors | 4003:Profile not queued for installation |  | S2 |
| 0x87D136B2 | -2016332110 |  | Service errors | 4002:Duplicate UUID |  | S2 |
| 0x87D136B1 | -2016332111 |  | Service errors | 4001:Installation failure |  | S2 |
| 0x87D136B0 | -2016332112 |  | Service errors | 4000:Cannot parse profile |  | S2 |
| 0x87D132C9 | -2016333111 |  | Service errors | 3001:Inconsistent value comparison sense (internal error) |  | S2 |
| 0x87D132C8 | -2016333112 |  | Service errors | 3000:Inconsistent restriction sense (internal error) |  | S2 |
| 0x87D12EE4 | -2016334108 |  | Service errors | 2004:Unsupported field value |  | S2 |
| 0x87D12EE3 | -2016334109 |  | Service errors | 2003:Bad data type in field |  | S2 |
| 0x87D12EE2 | -2016334110 |  | Service errors | 2002:Missing required field |  | S2 |
| 0x87D12EE1 | -2016334111 |  | Service errors | 2001:Unsupported payload version |  | S2 |
| 0x87D12EE0 | -2016334112 |  | Service errors | 2000:Malformed Payload |  | S2 |
| 0x87D12B02 | -2016335102 |  | Service errors | 1010:Unsupported field value |  | S2 |
| 0x87D12B01 | -2016335103 |  | Service errors | 1009:Profile installation failure |  | S2 |
| 0x87D12B00 | -2016335104 |  | Service errors | 1008:Non-unique payload identifiers |  | S2 |
| 0x87D12AFF | -2016335105 |  | Service errors | 1007:Non-unique UUIDs |  | S2 |
| 0x87D12AFE | -2016335106 |  | Service errors | 1006:Cannot decrypt |  | S2 |
| 0x87D12AFD | -2016335107 |  | Service errors | 1005:Empty profile |  | S2 |
| 0x87D12AFC | -2016335108 |  | Service errors | 1004:Bad signature |  | S2 |
| 0x87D12AFB | -2016335109 |  | Service errors | 1003:Bad data type in field |  | S2 |
| 0x87D12AFA | -2016335110 |  | Service errors | 1002:Missing required field |  | S2 |
| 0x87D12AF9 | -2016335111 |  | Service errors | 1001:Unsupported profile version |  | S2 |
| 0x87D12AF8 | -2016335112 |  | Service errors | 1000:Malformed profile |  | S2 |
| 0x87D10838 | -2016344008 |  | OMA response codes | (1404): Certificate access denied |  | S2 |
| 0x87D10837 | -2016344009 |  | OMA response codes | (1403): Certificate not found |  | S2 |
| 0x87D10836 | -2016344010 |  | OMA response codes | DCMO(1402): The Operation failed |  | S2 |
| 0x87D10835 | -2016344011 |  | OMA response codes | DCMO(1401): User chose not to accept the operation when prompted |  | S2 |
| 0x87D10834 | -2016344012 |  | OMA response codes | DCMO(1400): Client error |  | S2 |
| 0x87D107D4 | -2016344108 |  | OMA response codes | DCMO(1204): Device Capability is disabled and User is allowed to re-enable it |  | S2 |
| 0x87D107D3 | -2016344109 |  | OMA response codes | DCMO(1203): Device Capability is disabled and User is not allowed to re-enable it |  | S2 |
| 0x87D107D2 | -2016344110 |  | OMA response codes | DCMO(1202): Enable operation is performed successfully but the Device Capability is currently detached |  | S2 |
| 0xF3FB4D95 | -2016344111 | Hex and status code differ in source (hex = -201634411) | OMA response codes | DCMO(1201): Enable operation is performed successfully and the Device Capability is currently attached |  | S2 |
| 0x87D107D0 | -2016344112 |  | OMA response codes | DCMO(1200): Operation is performed successfully |  | S2 |
| 0x87D10205 | -2016345595 |  | OMA response codes | Syncml(517): The response to an atomic command was too large to fit in a single message. |  | S2 |
| 0x87D10204 | -2016345596 |  | OMA response codes | Syncml(516): Command was inside Atomic element and Atomic failed. This command was not rolled back successfully. |  | S2 |
| 0x87D10202 | -2016345598 |  | OMA response codes | Syncml(514): The SyncML command was not completed successfully, since the operation was already canceled before processing the command. |  | S2 |
| 0x87D10201 | -2016345599 |  | OMA response codes | Syncml(513): The recipient does not support or refuses to support the specified version of the SyncML Synchronization Protocol used in the request SyncML Message. |  | S2 |
| 0x87D10200 | -2016345600 |  | OMA response codes | Syncml(512): An application error occurred during the synchronization session. |  | S2 |
| 0x87D101FF | -2016345601 |  | OMA response codes | Syncml(511): A severe error occurred in the server while processing the request. |  | S2 |
| 0x87D101FE | -2016345602 |  | OMA response codes | Syncml(510): An error occurred while processing the request. The error is related to a failure in the recipient data store. |  | S2 |
| 0x87D101FD | -2016345603 |  | OMA response codes | Syncml(509): Reserved for future use. |  | S2 |
| 0x87D101FC | -2016345604 |  | OMA response codes | Syncml(508): An error occurred that necessitates a refresh of the current synchronization state of the client with the server. |  | S2 |
| 0x87D101FB | -2016345605 |  | OMA response codes | Syncml(507): The error caused all SyncML commands within an Atomic element type to fail. |  | S2 |
| 0x87D101FA | -2016345606 |  | OMA response codes | Syncml(506): An application error occurred while processing the request. |  | S2 |
| 0x87D101F9 | -2016345607 |  | OMA response codes | Syncml(505): The recipient does not support or refuses to support the specified version of SyncML DTD used in the request SyncML Message. |  | S2 |
| 0x87D101F7 | -2016345609 |  | OMA response codes | Syncml(503): The recipient is currently unable to handle the request due to a temporary overloading or maintenance of the recipient. |  | S2 |
| 0x87D101F6 | -2016345610 |  | OMA response codes | Syncml(502): The recipient, while acting as a gateway or proxy, received an invalid response from the upstream recipient it accessed in attempting to fulfill the request. |  | S2 |
| 0x87D101F5 | -2016345611 |  | OMA response codes | Syncml(501): The recipient does not support the command required to fulfill the request. |  | S2 |
| 0x87D101F4 | -2016345612 |  | OMA response codes | Syncml(500): The recipient encountered an unexpected condition which prevented it from fulfilling the request |  | S2 |
| 0x87D101AC | -2016345684 |  | OMA response codes | Syncml(428): Move failed |  | S2 |
| 0x87D101AB | -2016345685 |  | OMA response codes | Syncml(427): Parent cannot be deleted since it contains children. |  | S2 |
| 0x87D101AA | -2016345686 |  | OMA response codes | Syncml(426): Partial item not accepted. |  | S2 |
| 0x87D101A9 | -2016345687 |  | OMA response codes | Syncml(425): The requested command failed because the sender does not have adequate access control permissions (ACL) on the recipient. |  | S2 |
| 0x87D101A8 | -2016345688 |  | OMA response codes | Syncml(424): The chunked object was received, but the size of the received object did not match the size declared within the first chunk. |  | S2 |
| 0x87D101A7 | -2016345689 |  | OMA response codes | Syncml(423): The requested command failed because the "Soft Deleted" item was previously "Hard Deleted" on the server. |  | S2 |
| 0x87D101A6 | -2016345690 |  | OMA response codes | Syncml(422): The requested command failed on the server because the CGI scripting in the LocURI was incorrectly formed. |  | S2 |
| 0x87D101A5 | -2016345691 |  | OMA response codes | Syncml(421): The requested command failed on the server because the specified search grammar was not known. |  | S2 |
| 0x87D101A4 | -2016345692 |  | OMA response codes | Syncml(420): The recipient has no more storage space for the remaining synchronization data. |  | S2 |
| 0x87D101A3 | -2016345693 |  | OMA response codes | Syncml(419): The client request created a conflict which was resolved by the server command winning. |  | S2 |
| 0x87D101A2 | -2016345694 |  | OMA response codes | Syncml(418): The requested Put or Add command failed because the target already exists. |  | S2 |
| 0x87D101A1 | -2016345695 |  | OMA response codes | Syncml(417): The request failed at this time and the originator should retry the request later. |  | S2 |
| 0x87D101A0 | -2016345696 |  | OMA response codes | Syncml(416): The request failed because the specified byte size in the request was too big. |  | S2 |
| 0x87D1019F | -2016345697 |  | OMA response codes | Syncml(415): Unsupported media type or format. |  | S2 |
| 0x87D1019E | -2016345698 |  | OMA response codes | Syncml(414): The requested command failed because the target URI is too long for what the recipient is able or willing to process. |  | S2 |
| 0x87D1019D | -2016345699 |  | OMA response codes | Syncml(413): The recipient is refusing to perform the requested command because the requested item is larger than the recipient is able or willing to process. |  | S2 |
| 0x87D1019C | -2016345700 |  | OMA response codes | Syncml(412): The requested command failed on the recipient because it was incomplete or incorrectly formed. |  | S2 |
| 0x87D1019B | -2016345701 |  | OMA response codes | Syncml(411): The requested command must be accompanied by byte size or length information in the Meta element type. |  | S2 |
| 0x87D1019A | -2016345702 |  | OMA response codes | Syncml(410): The requested target is no longer on the recipient and no forwarding URI is known. |  | S2 |
| 0x87D10199 | -2016345703 |  | OMA response codes | Syncml(409): The requested failed because of an update conflict between the client and server versions of the data. |  | S2 |
| 0x87D10198 | -2016345704 |  | OMA response codes | Syncml(408): An expected message was not received within the required period of time. |  | S2 |
| 0x87D10197 | -2016345705 |  | OMA response codes | Syncml(407): The requested command failed because the originator must provide proper authentication. |  | S2 |
| 0x87D10196 | -2016345706 |  | OMA response codes | Syncml(406): The requested command failed because an optional feature in the request was not supported. |  | S2 |
| 0x87D10195 | -2016345707 |  | OMA response codes | Syncml(405): The requested command is not allowed on the target. |  | S2 |
| 0x87D10194 | -2016345708 |  | OMA response codes | Syncml(404): The requested target was not found. |  | S2 |
| 0x87D10193 | -2016345709 |  | OMA response codes | Syncml(403): The requested command failed, but the recipient understood the requested command. |  | S2 |
| 0x87D10192 | -2016345710 |  | OMA response codes | Syncml(402): The requested command failed because proper payment is needed. |  | S2 |
| 0x87D10191 | -2016345711 |  | OMA response codes | Syncml(401): The requested command failed because the requestor must provide proper authentication. |  | S2 |
| 0x87D10190 | -2016345712 |  | OMA response codes | Syncml(400): The requested command could not be performed because of malformed syntax in the command. |  | S2 |
| 0x87D10131 | -2016345807 |  | OMA response codes | Syncml(305): The requested target must be accessed through the specified proxy URI. |  | S2 |
| 0x87D10130 | -2016345808 |  | OMA response codes | Syncml(304):The requested SyncML command was not executed on the target. |  | S2 |
| 0x87D1012F | -2016345809 |  | OMA response codes | Syncml(303): The requested target can be found at another URI. |  | S2 |
| 0x87D1012E | -2016345810 |  | OMA response codes | Syncml(302): The requested target has temporarily moved to a different URI. |  | S2 |
| 0x87D1012D | -2016345811 |  | OMA response codes | Syncml(301): The requested target has a new URI. |  | S2 |
| 0x87D1012C | -2016345812 |  | OMA response codes | Syncml(300): The requested target is one of a number of multiple alternatives requested target. |  | S2 |
| 0x87D100D8 | -2016345896 |  | OMA response codes | Syncml(216): A command was inside Atomic element and Atomic failed. This command was rolled back successfully. |  | S2 |
| 0x87D100D7 | -2016345897 |  | OMA response codes | Syncml(215): A command was not executed, as a result of user interaction and user chose not to accept the choice. |  | S2 |
| 0x87D100D6 | -2016345898 |  | OMA response codes | Syncml(214): Operation canceled. The SyncML command completed successfully, but no more commands will be processed within the session. |  | S2 |
| 0x87D100D5 | -2016345899 |  | OMA response codes | Syncml(213): Chunked item accepted and buffered |  | S2 |
| 0x87D100D4 | -2016345900 |  | OMA response codes | Syncml(212): Authentication accepted. No further authentication is needed for the remainder of the synchronization session. This response code can only be used in response to a request in which the credentials were provided. |  | S2 |
| 0x87D100D3 | -2016345901 |  | OMA response codes | Syncml(211): Item not deleted. The requested item was not found. It could have been previously deleted. |  | S2 |
| 0x87D100D2 | -2016345902 |  | OMA response codes | Syncml(210): Delete without archive. The response indicates that the requested data was successfully deleted, but that it was not archived prior to deletion because this OPTIONAL feature was not supported by the implementation. |  | S2 |
| 0x87D100D1 | -2016345903 |  | OMA response codes | Conflict resolved with duplicate. The response indicates that the request created an update conflict; which was resolved with a duplication of the client's data being created in the server database. The response includes both the target URI of the duplicate in the Item of the Status. In addition, in the case of a two-way synchronization, an Add command is returned with the duplicate data definition. |  | S2 |
| 0x87D100D0 | -2016345904 |  | OMA response codes | Conflict resolved with client's command "winning". The response indicates that there was an update conflict; which was resolved by the client command winning. |  | S2 |
| 0x87D100CF | -2016345905 |  | OMA response codes | Conflict resolved with merge. The response indicates that the request created a conflict; which was resolved with a merge of the client and server instances of the data. The response includes both the Target and Source URLs in the Item of the Status. In addition, a Replace command is returned with the merged data. |  | S2 |
| 0x87D100CE | -2016345906 |  | OMA response codes | The response indicates that only part of the command was completed. If the remainder of the command can be completed later, then when completed another appropriate completion request status code SHOULD be created. |  | S2 |
| 0x87D100CD | -2016345907 |  | OMA response codes | The source SHOULD update their content. The originator of the request is being told that their content SHOULD be synchronized to get an up-to-date version. |  | S2 |
| 0x87D100CC | -2016345908 |  | OMA response codes | The request was successfully completed but no data is being returned. The response code is also returned in response to a Get when the target has no content. |  | S2 |
| 0x87D100CB | -2016345909 |  | OMA response codes | Non-authoritative response. The request is being responded to by an entity other than the one targeted. The response is only to be returned when the request would have been resulted in a 200 response code from the authoritative target. |  | S2 |
| 0x87D100CA | -2016345910 |  | OMA response codes | Accepted for processing. The request to either run a remote execution of an application or to alert a user or application was successfully performed. |  | S2 |
| 0x87D100C9 | -2016345911 |  | OMA response codes | The requested item was added. |  | S2 |
| 0x87D100C8 | -2016345912 |  | OMA response codes | The SyncML command completed successfully. |  | S2 |
| 0x87D10065 | -2016346011 |  | OMA response codes | The specified SyncML command is being carried out, but has not yet completed. |  | S2 |
|  |  | Windows error 0 (ERROR_SUCCESS) | Windows Installer |  | The action completed successfully. | S3 |
| 0x8007000D | -2147024883 | Windows error 13 (ERROR_INVALID_DATA) | Windows Installer |  | The data is invalid. | S3 |
| 0x80070057 | -2147024809 | Windows error 87 (ERROR_INVALID_PARAMETER) | Windows Installer |  | One of the parameters was invalid. | S3 |
| 0x80070078 | -2147024776 | Windows error 120 (ERROR_CALL_NOT_IMPLEMENTED) | Windows Installer |  | This value is returned when a custom action attempts to call a function that can't be called from custom actions. The function returns the value ERROR_CALL_NOT_IMPLEMENTED. | S3 |
| 0x800704EB | -2147023637 | Windows error 1259 (ERROR_APPHELP_BLOCK) | Windows Installer |  | If Windows Installer determines a product might be incompatible with the current operating system, it displays a dialog box informing the user and asking whether to try to install anyway. This error code is returned if the user chooses not to try the installation. | S3 |
| 0x80070641 | -2147023295 | Windows error 1601 (ERROR_INSTALL_SERVICE_FAILURE) | Windows Installer |  | The Windows Installer service couldn't be accessed. Contact your support personnel to verify that the Windows Installer service is properly registered. | S3 |
| 0x80070642 | -2147023294 | Windows error 1602 (ERROR_INSTALL_USEREXIT) | Windows Installer |  | The user canceled installation. | S3 |
| 0x80070643 | -2147023293 | Windows error 1603 (ERROR_INSTALL_FAILURE) | Windows Installer |  | A fatal error occurred during installation. | S3 |
| 0x80070644 | -2147023292 | Windows error 1604 (ERROR_INSTALL_SUSPEND) | Windows Installer |  | Installation suspended, incomplete. | S3 |
| 0x80070645 | -2147023291 | Windows error 1605 (ERROR_UNKNOWN_PRODUCT) | Windows Installer |  | This action is only valid for products that are currently installed. | S3 |
| 0x80070646 | -2147023290 | Windows error 1606 (ERROR_UNKNOWN_FEATURE) | Windows Installer |  | The feature identifier isn't registered. | S3 |
| 0x80070647 | -2147023289 | Windows error 1607 (ERROR_UNKNOWN_COMPONENT) | Windows Installer |  | The component identifier isn't registered. | S3 |
| 0x80070648 | -2147023288 | Windows error 1608 (ERROR_UNKNOWN_PROPERTY) | Windows Installer |  | This is an unknown property. | S3 |
| 0x80070649 | -2147023287 | Windows error 1609 (ERROR_INVALID_HANDLE_STATE) | Windows Installer |  | The handle is in an invalid state. | S3 |
| 0x8007064A | -2147023286 | Windows error 1610 (ERROR_BAD_CONFIGURATION) | Windows Installer |  | The configuration data for this product is corrupt. Contact your support personnel. | S3 |
| 0x8007064B | -2147023285 | Windows error 1611 (ERROR_INDEX_ABSENT) | Windows Installer |  | The component qualifier not present. | S3 |
| 0x8007064C | -2147023284 | Windows error 1612 (ERROR_INSTALL_SOURCE_ABSENT) | Windows Installer |  | The installation source for this product isn't available. Verify that the source exists and that you can access it. | S3 |
| 0x8007064D | -2147023283 | Windows error 1613 (ERROR_INSTALL_PACKAGE_VERSION) | Windows Installer |  | This installation package can't be installed by the Windows Installer service. You must install a Windows service pack that contains a newer version of the Windows Installer service. | S3 |
| 0x8007064E | -2147023282 | Windows error 1614 (ERROR_PRODUCT_UNINSTALLED) | Windows Installer |  | The product is uninstalled. | S3 |
| 0x8007064F | -2147023281 | Windows error 1615 (ERROR_BAD_QUERY_SYNTAX) | Windows Installer |  | The SQL query syntax is invalid or unsupported. | S3 |
| 0x80070650 | -2147023280 | Windows error 1616 (ERROR_INVALID_FIELD) | Windows Installer |  | The record field does not exist. | S3 |
| 0x80070652 | -2147023278 | Windows error 1618 (ERROR_INSTALL_ALREADY_RUNNING) | Windows Installer |  | Another installation is already in progress. Complete that installation before proceeding with this install. For information about the mutex, see _MSIExecute Mutex. | S3 |
| 0x80070653 | -2147023277 | Windows error 1619 (ERROR_INSTALL_PACKAGE_OPEN_FAILED) | Windows Installer |  | This installation package couldn't be opened. Verify that the package exists and is accessible, or contact the application vendor to verify that this is a valid Windows Installer package. | S3 |
| 0x80070654 | -2147023276 | Windows error 1620 (ERROR_INSTALL_PACKAGE_INVALID) | Windows Installer |  | This installation package couldn't be opened. Contact the application vendor to verify that this is a valid Windows Installer package. | S3 |
| 0x80070655 | -2147023275 | Windows error 1621 (ERROR_INSTALL_UI_FAILURE) | Windows Installer |  | There was an error starting the Windows Installer service user interface. Contact your support personnel. | S3 |
| 0x80070656 | -2147023274 | Windows error 1622 (ERROR_INSTALL_LOG_FAILURE) | Windows Installer |  | There was an error opening installation log file. Verify that the specified log file location exists and is writable. | S3 |
| 0x80070657 | -2147023273 | Windows error 1623 (ERROR_INSTALL_LANGUAGE_UNSUPPORTED) | Windows Installer |  | This language of this installation package isn't supported by your system. | S3 |
| 0x80070658 | -2147023272 | Windows error 1624 (ERROR_INSTALL_TRANSFORM_FAILURE) | Windows Installer |  | There was an error applying transforms. Verify that the specified transform paths are valid. | S3 |
| 0x80070659 | -2147023271 | Windows error 1625 (ERROR_INSTALL_PACKAGE_REJECTED) | Windows Installer |  | This installation is forbidden by system policy. Contact your system administrator. | S3 |
| 0x8007065A | -2147023270 | Windows error 1626 (ERROR_FUNCTION_NOT_CALLED) | Windows Installer |  | The function couldn't be executed. | S3 |
| 0x8007065B | -2147023269 | Windows error 1627 (ERROR_FUNCTION_FAILED) | Windows Installer |  | The function failed during execution. | S3 |
| 0x8007065C | -2147023268 | Windows error 1628 (ERROR_INVALID_TABLE) | Windows Installer |  | An invalid or unknown table was specified. | S3 |
| 0x8007065D | -2147023267 | Windows error 1629 (ERROR_DATATYPE_MISMATCH) | Windows Installer |  | The data supplied is the wrong type. | S3 |
| 0x8007065E | -2147023266 | Windows error 1630 (ERROR_UNSUPPORTED_TYPE) | Windows Installer |  | Data of this type isn't supported. | S3 |
| 0x8007065F | -2147023265 | Windows error 1631 (ERROR_CREATE_FAILED) | Windows Installer |  | The Windows Installer service failed to start. Contact your support personnel. | S3 |
| 0x80070660 | -2147023264 | Windows error 1632 (ERROR_INSTALL_TEMP_UNWRITABLE) | Windows Installer |  | The Temp folder is either full or inaccessible. Verify that the *Temp* folder exists and that you can write to it. | S3 |
| 0x80070661 | -2147023263 | Windows error 1633 (ERROR_INSTALL_PLATFORM_UNSUPPORTED) | Windows Installer |  | This installation package isn't supported on this platform. Contact your application vendor. | S3 |
| 0x80070662 | -2147023262 | Windows error 1634 (ERROR_INSTALL_NOTUSED) | Windows Installer |  | Component isn't used on this machine. | S3 |
| 0x80070663 | -2147023261 | Windows error 1635 (ERROR_PATCH_PACKAGE_OPEN_FAILED) | Windows Installer |  | This patch package couldn't be opened. Verify that the patch package exists and is accessible, or contact the application vendor to verify that this is a valid Windows Installer patch package. | S3 |
| 0x80070664 | -2147023260 | Windows error 1636 (ERROR_PATCH_PACKAGE_INVALID) | Windows Installer |  | This patch package couldn't be opened. Contact the application vendor to verify that this is a valid Windows Installer patch package. | S3 |
| 0x80070665 | -2147023259 | Windows error 1637 (ERROR_PATCH_PACKAGE_UNSUPPORTED) | Windows Installer |  | This patch package can't be processed by the Windows Installer service. You must install a Windows service pack that contains a newer version of the Windows Installer service. | S3 |
| 0x80070666 | -2147023258 | Windows error 1638 (ERROR_PRODUCT_VERSION) | Windows Installer |  | Another version of this product is already installed. Installation of this version can't continue. To configure or remove the existing version of this product, use Add/Remove Programs in Control Panel. | S3 |
| 0x80070667 | -2147023257 | Windows error 1639 (ERROR_INVALID_COMMAND_LINE) | Windows Installer |  | Invalid command line argument. Consult the Windows Installer SDK for detailed command-line help. | S3 |
| 0x80070668 | -2147023256 | Windows error 1640 (ERROR_INSTALL_REMOTE_DISALLOWED) | Windows Installer |  | The current user isn't permitted to perform installations from a client session of a server running the Terminal Server role service. | S3 |
| 0x80070669 | -2147023255 | Windows error 1641 (ERROR_SUCCESS_REBOOT_INITIATED) | Windows Installer |  | The installer has initiated a restart. This message indicates success. | S3 |
| 0x8007066A | -2147023254 | Windows error 1642 (ERROR_PATCH_TARGET_NOT_FOUND) | Windows Installer |  | The installer can't install the upgrade patch because the program being upgraded may be missing or the upgrade patch updates a different version of the program. Verify that the program to be upgraded exists on your computer and that you have the correct upgrade patch. | S3 |
| 0x8007066B | -2147023253 | Windows error 1643 (ERROR_PATCH_PACKAGE_REJECTED) | Windows Installer |  | The patch package isn't permitted by system policy. | S3 |
| 0x8007066C | -2147023252 | Windows error 1644 (ERROR_INSTALL_TRANSFORM_REJECTED) | Windows Installer |  | One or more customizations aren't permitted by system policy. | S3 |
| 0x8007066D | -2147023251 | Windows error 1645 (ERROR_INSTALL_REMOTE_PROHIBITED) | Windows Installer |  | Windows Installer doesn't permit installation from a Remote Desktop Connection. | S3 |
| 0x8007066E | -2147023250 | Windows error 1646 (ERROR_PATCH_REMOVAL_UNSUPPORTED) | Windows Installer |  | The patch package isn't a removable patch package. | S3 |
| 0x8007066F | -2147023249 | Windows error 1647 (ERROR_UNKNOWN_PATCH) | Windows Installer |  | The patch isn't applied to this product. | S3 |
| 0x80070670 | -2147023248 | Windows error 1648 (ERROR_PATCH_NO_SEQUENCE) | Windows Installer |  | No valid sequence could be found for the set of patches. | S3 |
| 0x80070671 | -2147023247 | Windows error 1649 (ERROR_PATCH_REMOVAL_DISALLOWED) | Windows Installer |  | Patch removal was disallowed by policy. | S3 |
| 0x80070672 | -2147023246 | Windows error 1650 (ERROR_INVALID_PATCH_XML) | Windows Installer |  | The XML patch data is invalid. | S3 |
| 0x80070673 | -2147023245 | Windows error 1651 (ERROR_PATCH_MANAGED_ADVERTISED_PRODUCT) | Windows Installer |  | Administrative user failed to apply patch for a per-user managed or a per-machine application that'is in advertised state. | S3 |
| 0x80070674 | -2147023244 | Windows error 1652 (ERROR_INSTALL_SERVICE_SAFEBOOT) | Windows Installer |  | Windows Installer isn't accessible when the computer is in *Safe Mode*. Exit Safe Mode and try again or try using system restore to return your computer to a previous state. Available beginning with Windows Installer version 4.0. | S3 |
| 0x80070675 | -2147023243 | Windows error 1653 (ERROR_ROLLBACK_DISABLED) | Windows Installer |  | Couldn't perform a multiple-package transaction because rollback has been disabled. Multiple-package installations can't run if rollback is disabled. Available beginning with Windows Installer version 4.5. | S3 |
| 0x80070676 | -2147023242 | Windows error 1654 (ERROR_INSTALL_REJECTED) | Windows Installer |  | The app that you're trying to run isn't supported on this version of Windows. A Windows Installer package, patch, or transform that has not been signed by Microsoft can't be installed on an ARM computer. | S3 |
| 0x80070BC2 | -2147021886 | Windows error 3010 (ERROR_SUCCESS_REBOOT_REQUIRED) | Windows Installer |  | A restart is required to complete the install. This message indicates success. This does not include installs where the ForceReboot action is run. | S3 |
| 0x80070002 | -2147024894 | E_FILENOTFOUND | Windows app packages (MSIX/AppX) |  | File or path is not found. This can occur during a COM typelib validation requires that the path for the directory actually exist within your MSIX package. | S4 |
| 0x8007000B | -2147024885 | ERROR_BAD_FORMAT | Windows app packages (MSIX/AppX) |  | The package isn't correctly formatted and needs to be re-built or re-signed. You may get this error if there is a mismatch between the signing certificate subject name and the AppxManifest.xml publisher name. See How to sign an app package using SignTool. | S4 |
| 0x80070057 | -2147024809 | E_INVALIDARG | Windows app packages (MSIX/AppX) |  | One or more arguments are not valid. If you check the AppXDeployment-Server event log and see the following event: "While installing the package, the system failed to register the windows.repositoryExtension extension due to the following error: The parameter is incorrect." You may get this error if the manifest elements DisplayName or Description contain characters disallowed by Windows firewall such as `/`, due to which Windows fails to create the AppContainer profile for the package. Please remove these characters from the manifest and try installing the package. | S4 |
| 0x80073CF0 | -2147009296 | ERROR_INSTALL_OPEN_ PACKAGE_FAILED | Windows app packages (MSIX/AppX) |  | The package couldn't be opened. Possible causes: The package is unsigned.; The publisher name doesn't match the signing certificate subject.; The file:// prefix is missing or the package couldn't be found at the specified location.For more information, check the AppxPackagingOM event log. | S4 |
| 0x80073CF1 | -2147009295 | ERROR_INSTALL_PACKAGE_ NOT_FOUND | Windows app packages (MSIX/AppX) |  | The package couldn't be found. You may get this error while removing a package that isn't installed for the current user. | S4 |
| 0x80073CF2 | -2147009294 | ERROR_INSTALL_INVALID_ PACKAGE | Windows app packages (MSIX/AppX) |  | The package data isn't valid. | S4 |
| 0x80073CF3 | -2147009293 | ERROR_INSTALL_RESOLVE_ DEPENDENCY_FAILED | Windows app packages (MSIX/AppX) |  | The package failed update, dependency, or conflict validation. Possible causes: The incoming package conflicts with an installed package.; A specified package dependency can't be found.; The package doesn't support the correct processor architecture.For more informtion, check the AppXDeployment-Server event log. | S4 |
| 0x80073CF4 | -2147009292 | ERROR_INSTALL_OUT_ OF_DISK_SPACE | Windows app packages (MSIX/AppX) |  | There isn't enough disk space on your computer. Free some space and try again. | S4 |
| 0x80073CF5 | -2147009291 | ERROR_INSTALL_NETWORK_ FAILURE | Windows app packages (MSIX/AppX) |  | The package can't be downloaded. | S4 |
| 0x80073CF6 | -2147009290 | ERROR_INSTALL_ REGISTRATION_FAILURE | Windows app packages (MSIX/AppX) |  | The package can't be registered. For more information, check the AppXDeployment-Server event log. | S4 |
| 0x80073CF7 | -2147009289 | ERROR_INSTALL_ DEREGISTRATION_EFAILURE | Windows app packages (MSIX/AppX) |  | The package can't be unregistered. You may get this error while removing a package. For more information, check the AppXDeployment-Server event log. | S4 |
| 0x80073CF8 | -2147009288 | ERROR_INSTALL_CANCEL | Windows app packages (MSIX/AppX) |  | The user canceled the install request. | S4 |
| 0x80073CF9 | -2147009287 | ERROR_INSTALL_FAILED | Windows app packages (MSIX/AppX) |  | Package install failed. Contact the software vendor. For more information, check the AppXDeployment-Server event log. | S4 |
| 0x80073CFA | -2147009286 | ERROR_REMOVE_FAILED | Windows app packages (MSIX/AppX) |  | Package removal failed. You may get this error for failures that occur during package uninstall. For more information, see RemovePackageAsync. | S4 |
| 0x80073CFB | -2147009285 | ERROR_PACKAGE_ ALREADY_EXISTS | Windows app packages (MSIX/AppX) |  | The provided package is already installed, and reinstallation of the package is blocked. You may get this error if installing a package that is not bitwise identical to the package that is already installed. Note that the digital signature is also part of the package. Hence if a package is rebuilt or resigned, it is no longer bitwise identical to the previously installed package. Two possible options to fix this error are: (1) Increment the version number of the app, then rebuild and resign the package (2) Remove the old package for every user on the system before installing the new package. | S4 |
| 0x80073CFC | -2147009284 | ERROR_NEEDS_REMEDIATION | Windows app packages (MSIX/AppX) |  | The app can't be started. Try reinstalling the app. | S4 |
| 0x80073CFD | -2147009283 | ERROR_INSTALL_ PREREQUISITE_FAILED | Windows app packages (MSIX/AppX) |  | A specified install prerequisite couldn't be satisfied. | S4 |
| 0x80073CFE | -2147009282 | ERROR_PACKAGE_ REPOSITORY_CORRUPTED | Windows app packages (MSIX/AppX) |  | The package repository is corrupted. You may get this error if the folder referenced by this registry key doesn't exist or is corrupted: HKLM\Software\Microsoft\Windows\ CurrentVersion\Appx\PackageRepositoryRoot To recover from this state, refresh your PC. | S4 |
| 0x80073CFF | -2147009281 | ERROR_INSTALL_ POLICY_FAILURE | Windows app packages (MSIX/AppX) |  | To install this app, you need a developer license or a sideloading-enabled system. You may get this error if the package doesn't meet one of the following requirements: The app is deployed using F5 in Visual Studio on a computer with a Windows developer license.; The package is signed with a Microsoft signature and deployed as part of Windows or from the Microsoft Store.; The package is signed with a trusted signature and installed on a computer with a developer license, a domain-joined computer with the AllowAllTrustedApps policy enabled, or a computer with a Windows Sideloading license with the AllowAllTrustedApps policy enabled. | S4 |
| 0x80073D00 | -2147009280 | ERROR_PACKAGE_UPDATING | Windows app packages (MSIX/AppX) |  | The app can't be started because it's currently updating. | S4 |
| 0x80073D01 | -2147009279 | ERROR_DEPLOYMENT_ BLOCKED_BY_POLICY | Windows app packages (MSIX/AppX) |  | The package deployment operation is blocked by policy. Contact your system administrator. Possible causes: Package deployment is blocked by Application Control Policies.; Package deployment is blocked by the "Allow deployment operations in special profiles" policy.One of the possible reasons is a need for a roaming profile. For information about setting up Roaming User Profiles on user accounts, see Deploy Roaming User Profiles. If there are no policies configured on your system and you still see this error, perhaps you are logged in with a temporary profile. Log out and log in again, then try the operation again. | S4 |
| 0x80073D02 | -2147009278 | ERROR_PACKAGES_IN_USE | Windows app packages (MSIX/AppX) |  | The package couldn't be installed because resources it modifies are currently in use. | S4 |
| 0x80073D03 | -2147009277 | ERROR_RECOVERY_ FILE_CORRUPT | Windows app packages (MSIX/AppX) |  | The package couldn't be recovered because data that's necessary for recovery is corrupted. | S4 |
| 0x80073D04 | -2147009276 | ERROR_INVALID_ STAGED_SIGNATURE | Windows app packages (MSIX/AppX) |  | The signature isn't valid. To register in developer mode, AppxSignature.p7x and AppxBlockMap.xml must be valid or shouldn't be present. If you are a developer using F5 with Visual Studio, ensure that your built project directory doesn't contain signature or block map files from previous versions of the package. | S4 |
| 0x80073D05 | -2147009275 | ERROR_DELETING_EXISTING_ APPLICATIONDATA_STORE_FAILED | Windows app packages (MSIX/AppX) |  | An error occurred while deleting the package's previously existing application data. You can get this error if the simulator is running. Close the simulator. You can also get this error if there are files open in the app data (for example, if you have a log file open in a text editor). | S4 |
| 0x80073D06 | -2147009274 | ERROR_INSTALL_ PACKAGE_DOWNGRADE | Windows app packages (MSIX/AppX) |  | The package couldn't be installed because a higher version of this package is already installed. | S4 |
| 0x80073D07 | -2147009273 | ERROR_SYSTEM_ NEEDS_REMEDIATION | Windows app packages (MSIX/AppX) |  | An error in a system binary was detected. To fix the problem, try refreshing the PC. | S4 |
| 0x80073D08 | -2147009272 | ERROR_APPX_INTEGRITY_ FAILURE_EXTERNAL | Windows app packages (MSIX/AppX) |  | A corrupted non-Windows binary was detected on the system. | S4 |
| 0x80073D09 | -2147009271 | ERROR_RESILIENCY_ FILE_CORRUPT | Windows app packages (MSIX/AppX) |  | The operation couldn't be resumed because data that's necessary for recovery is corrupted. | S4 |
| 0x80073D0A | -2147009270 | ERROR_INSTALL_FIREWALL_ SERVICE_NOT_RUNNING | Windows app packages (MSIX/AppX) |  | The package couldn't be installed because the Windows Firewall service isn't running. Enable the Windows Firewall service and try again. | S4 |
| 0x80073D0B | -2147009269 | ERROR_PACKAGE_MOVE_FAILED | Windows app packages (MSIX/AppX) |  | The package move operation failed. | S4 |
| 0x80073D0C | -2147009268 | ERROR_INSTALL_VOLUME_ NOT_EMPTY | Windows app packages (MSIX/AppX) |  | The deployment operation failed because the volume is not empty. | S4 |
| 0x80073D0D | -2147009267 | ERROR_INSTALL_VOLUME_ OFFLINE | Windows app packages (MSIX/AppX) |  | The deployment operation failed because the volume is offline. For a package update, the volume refers to the installed volume of all package versions. | S4 |
| 0x80073D0E | -2147009266 | ERROR_INSTALL_VOLUME_ CORRUPT | Windows app packages (MSIX/AppX) |  | The deployment operation failed because the specified volume is corrupt. | S4 |
| 0x80073D0F | -2147009265 | ERROR_NEEDS_REGISTRATION | Windows app packages (MSIX/AppX) |  | The deployment operation failed because the specified application needs to be registered first. | S4 |
| 0x80073D10 | -2147009264 | ERROR_INSTALL_WRONG_ PROCESSOR_ARCHITECTURE | Windows app packages (MSIX/AppX) |  | The deployment operation failed because the package targets the wrong processor architecture. | S4 |
| 0x80073D11 | -2147009263 | ERROR_DEV_SIDELOAD_ LIMIT_EXCEEDED | Windows app packages (MSIX/AppX) |  | You have reached the maximum number of developer sideloaded packages allowed on this device. Please uninstall a sideloaded package and try again. | S4 |
| 0x80073D12 | -2147009262 | ERROR_INSTALL_OPTIONAL_ PACKAGE_REQUIRES_ MAIN_PACKAGE | Windows app packages (MSIX/AppX) |  | A main app package is required to install this optional package. Install the main package first and try again. | S4 |
| 0x80073D13 | -2147009261 | ERROR_PACKAGE_NOT_ SUPPORTED_ON_FILESYSTEM | Windows app packages (MSIX/AppX) |  | This app package type is not supported on this filesystem. | S4 |
| 0x80073D14 | -2147009260 | ERROR_PACKAGE_MOVE_ BLOCKED_BY_STREAMING | Windows app packages (MSIX/AppX) |  | Package move operation is blocked until the application has finished streaming. | S4 |
| 0x80073D15 | -2147009259 | ERROR_INSTALL_OPTIONAL_ PACKAGE_APPLICATIONID_ NOT_UNIQUE | Windows app packages (MSIX/AppX) |  | A main or another optional app package has the same application ID as this optional package. Change the application ID for the optional package to avoid conflicts. | S4 |
| 0x80073D16 | -2147009258 | ERROR_PACKAGE_STAGING_ ONHOLD | Windows app packages (MSIX/AppX) |  | This staging session has been held to allow another staging operation to be prioritized. | S4 |
| 0x80073D17 | -2147009257 | ERROR_INSTALL_INVALID_ RELATED_SET_UPDATE | Windows app packages (MSIX/AppX) |  | A related set cannot be updated because the updated set is invalid. All packages in the related set must be updated at the same time. | S4 |
| 0x80073D18 | -2147009256 | ERROR_INSTALL_OPTIONAL_ PACKAGE_REQUIRES_MAIN_ PACKAGE_FULLTRUST_CAPABILITY | Windows app packages (MSIX/AppX) |  | An optional package with a FullTrust entry point requires the main package to have the runFullTrust capability. | S4 |
| 0x80073D19 | -2147009255 | ERROR_DEPLOYMENT_BLOCKED_ BY_USER_LOG_OFF | Windows app packages (MSIX/AppX) |  | An error occurred because a user was logged off. | S4 |
| 0x80073D1A | -2147009254 | ERROR_PROVISION_OPTIONAL_ PACKAGE_REQUIRES_MAIN_ PACKAGE_PROVISIONED | Windows app packages (MSIX/AppX) |  | An optional package provision requires the dependency main package to also be provisioned. | S4 |
| 0x80073D1B | -2147009253 | ERROR_PACKAGES_REPUTATION_ CHECK_FAILED | Windows app packages (MSIX/AppX) |  | The packages failed the SmartScreen reputation check. | S4 |
| 0x80073D1C | -2147009252 | ERROR_PACKAGES_REPUTATION_ CHECK_TIMEDOUT | Windows app packages (MSIX/AppX) |  | The SmartScreen reputation check operation timed out. | S4 |
| 0x80073D1D | -2147009251 | ERROR_DEPLOYMENT_OPTION_ NOT_SUPPORTED | Windows app packages (MSIX/AppX) |  | The current deployment option is not supported. | S4 |
| 0x80073D1E | -2147009250 | ERROR_APPINSTALLER_ ACTIVATION_BLOCKED | Windows app packages (MSIX/AppX) |  | Activation is blocked due to the .appinstaller update settings for this app. | S4 |
| 0x80073D1F | -2147009249 | ERROR_REGISTRATION_FROM_ REMOTE_DRIVE_NOT_SUPPORTED | Windows app packages (MSIX/AppX) |  | Remote drives are not supported. Use \\server\share to register a remote package. | S4 |
| 0x80073D20 | -2147009248 | ERROR_APPX_RAW_ DATA_WRITE_FAILED | Windows app packages (MSIX/AppX) |  | Failed to process and write downloaded package data to disk. | S4 |
| 0x80073D21 | -2147009247 | ERROR_DEPLOYMENT_BLOCKED_ BY_VOLUME_POLICY_PACKAGE | Windows app packages (MSIX/AppX) |  | The deployment operation was blocked due to a per-package-family policy restricting deployments on a non-system volume. Per policy, this app must be installed to the system drive, but that's not set as the default. In Storage settings, make the system drive the default location to save new content, then retry the install. | S4 |
| 0x80073D22 | -2147009246 | ERROR_DEPLOYMENT_BLOCKED_ BY_VOLUME_POLICY_MACHINE | Windows app packages (MSIX/AppX) |  | The deployment operation was blocked due to a machine-wide policy restricting deployments on a non-system volume. Per policy, this app must be installed to the system drive, but that's not set as the default. In Storage settings, make the system drive the default location to save new content, then retry the install. | S4 |
| 0x80073D23 | -2147009245 | ERROR_DEPLOYMENT_BLOCKED_ BY_PROFILE_POLICY | Windows app packages (MSIX/AppX) |  | The deployment operation was blocked because special profile deployment is not allowed (special profiles are user profiles where changes are discarded after the user signs out). Try logging into an account that is not a special profile. You can try logging out and logging back into the current account, or try logging into a different account. | S4 |
| 0x80073D24 | -2147009244 | ERROR_DEPLOYMENT_FAILED_ CONFLICTING_MUTABLE_PACKAGE_ DIRECTORY | Windows app packages (MSIX/AppX) |  | The deployment operation failed due to a conflicting package's mutable package directory. To install this package, remove the existing package with the conflicting mutable package directory. | S4 |
| 0x80073D25 | -2147009243 | ERROR_SINGLETON_RESOURCE_ INSTALLED_IN_ACTIVE_USER | Windows app packages (MSIX/AppX) |  | The package installation failed because a singleton resource was specified and another user with that package installed is logged in. Make sure that all active users with the package installed are logged out and retry installation. | S4 |
| 0x80073D26 | -2147009242 | ERROR_DIFFERENT_VERSION_ OF_PACKAGED_SERVICE_INSTALLED | Windows app packages (MSIX/AppX) |  | The package installation failed because a different version of the service is installed. Try installing a newer version of the package. | S4 |
| 0x80073D27 | -2147009241 | ERROR_SERVICE_EXISTS_ AS_NON_PACKAGED_SERVICE | Windows app packages (MSIX/AppX) |  | The package installation failed because a version of the service exists outside of an .msix/.appx package. Contact your software vendor. | S4 |
| 0x80073D28 | -2147009240 | ERROR_PACKAGED_SERVICE_ REQUIRES_ADMIN_PRIVILEGES | Windows app packages (MSIX/AppX) |  | The package installation failed because administrator privileges are required. Contact an administrator to install this package. | S4 |
| 0x80073D29 | -2147009239 | ERROR_REDIRECTION_TO_ DEFAULT_ACCOUNT_NOT_ALLOWED | Windows app packages (MSIX/AppX) |  | The package deployment failed because the operation would have redirected to default account, when the caller said not to do so. | S4 |
| 0x80073D2A | -2147009238 | ERROR_PACKAGE_LACKS_ CAPABILITY_TO_DEPLOY_ON_HOST | Windows app packages (MSIX/AppX) |  | The package deployment failed because the package requires a capability to natively target this host. | S4 |
| 0x80073D2B | -2147009237 | ERROR_UNSIGNED_PACKAGE_ INVALID_CONTENT | Windows app packages (MSIX/AppX) |  | The package deployment failed because its content is not valid for an unsigned package. | S4 |
| 0x80073D2C | -2147009236 | ERROR_UNSIGNED_PACKAGE_ INVALID_PUBLISHER_NAMESPACE | Windows app packages (MSIX/AppX) |  | The package deployment failed because its publisher is not in the unsigned namespace. | S4 |
| 0x80073D2D | -2147009235 | ERROR_SIGNED_PACKAGE_ INVALID_PUBLISHER_NAMESPACE | Windows app packages (MSIX/AppX) |  | The package deployment failed because its publisher is not in the signed namespace. | S4 |
| 0x80073D2E | -2147009234 | ERROR_PACKAGE_EXTERNAL_ LOCATION_NOT_ALLOWED | Windows app packages (MSIX/AppX) |  | The package deployment failed because its publisher is not in the signed namespace. | S4 |
| 0x80073D2F | -2147009233 | ERROR_INSTALL_FULLTRUST_ HOSTRUNTIME_REQUIRES_MAIN_ PACKAGE_FULLTRUST_CAPABILITY | Windows app packages (MSIX/AppX) |  | A host runtime dependency resolving to a package with full trust content requires the main package to have the runFullTrust capability. | S4 |
| 0x80073D3F | -2147009217 | ERROR_INSTALL_DRIVE_ NOT_FOUND | Windows app packages (MSIX/AppX) |  | The drive referenced during package deployment couldn't be found. If you previously set apps to install on an external or secondary drive, make sure it's connected and accessible. You can change the default install location in Settings > System > Storage > Change where new content is saved. | S4 |
| 0x80080200 | -2146958848 | APPX_E_PACKAGING_INTERNAL | Windows app packages (MSIX/AppX) |  | The packaging API has encountered an internal error. | S4 |
| 0x80080201 | -2146958847 | APPX_E_INTERLEAVING_ NOT_ALLOWED | Windows app packages (MSIX/AppX) |  | The package isn't valid because its contents are interleaved. | S4 |
| 0x80080202 | -2146958846 | APPX_E_RELATIONSHIPS_ NOT_ALLOWED | Windows app packages (MSIX/AppX) |  | The package isn't valid because it contains OPC relationships. | S4 |
| 0x80080203 | -2146958845 | APPX_E_MISSING_ REQUIRED_FILE | Windows app packages (MSIX/AppX) |  | The package isn't valid because it's missing a manifest or block map, or a code integrity file is present but a signature file is missing. Ensure that the package isn't missing one or more of these required files: \AppxManifest.xml; \AppxBlockMap.xmlIf the package contains \AppxMetadata\CodeIntegrity.cat, it must also contain \AppxSignature.p7x. | S4 |
| 0x80080204 | -2146958844 | APPX_E_INVALID_MANIFEST | Windows app packages (MSIX/AppX) |  | The package's AppxManifest.xml file isn't valid. | S4 |
| 0x80080205 | -2146958843 | APPX_E_INVALID_BLOCKMAP | Windows app packages (MSIX/AppX) |  | The package's AppxBlockMap.xml file isn't valid. | S4 |
| 0x80080206 | -2146958842 | APPX_E_CORRUPT_CONTENT | Windows app packages (MSIX/AppX) |  | The package contents can't be read because it's corrupted. | S4 |
| 0x80080207 | -2146958841 | APPX_E_BLOCK_ HASH_INVALID | Windows app packages (MSIX/AppX) |  | The computed hash value of the block doesn't match the has value stored in the block map. | S4 |
| 0x80080208 | -2146958840 | APPX_E_REQUESTED_ RANGE_TOO_LARGE | Windows app packages (MSIX/AppX) |  | The requested byte range is over 4 GB when translated to a byte range of blocks. | S4 |
| 0x800B0100 | -2146762496 | TRUST_E_NOSIGNATURE | Windows app packages (MSIX/AppX) |  | No signature is present in the subject. You may get this error if the package is unsigned or the signature isn't valid. The package must be signed to be deployed. | S4 |
| 0x800B0109 | -2146762487 | CERT_E_UNTRUSTEDROOT | Windows app packages (MSIX/AppX) |  | A certificate chain processed, but terminated in a root certificate which isn't trusted by the trust provider. See Signing a package. | S4 |
| 0x800B010A | -2146762486 | CERT_E_CHAINING | Windows app packages (MSIX/AppX) |  | A certificate chain couldn't be built to a trusted root certification authority. See Signing a package. | S4 |
| 0x80080209 | -2146958839 | APPX_E_INVALID_ SIP_CLIENT_DATA | Windows app packages (MSIX/AppX) |  | The SIP_SUBJECTINFOstructure used to sign the package didn't contain the required data | S4 |
| 0x8008020A | -2146958838 | APPX_E_INVALID_ KEY_INFO | Windows app packages (MSIX/AppX) |  | The APPX_KEY_INFO structure used to encrypt or decrypt the package contains invalid data. | S4 |
| 0x8008020B | -2146958837 | APPX_E_INVALID_ CONTENTGROUPMAP | Windows app packages (MSIX/AppX) |  | The .msix/.appx package's content group map is invalid. | S4 |
| 0x8008020C | -2146958836 | APPX_E_INVALID_ APPINSTALLER | Windows app packages (MSIX/AppX) |  | The .appinstaller file for the package is invalid. | S4 |
| 0x8008020D | -2146958835 | APPX_E_DELTA_BASELINE_ VERSION_MISMATCH | Windows app packages (MSIX/AppX) |  | The baseline package version in delta package does not match the version in the baseline package to be updated. | S4 |
| 0x8008020E | -2146958834 | APPX_E_DELTA_PACKAGE_ MISSING_FILE | Windows app packages (MSIX/AppX) |  | The delta package is missing a file from the updated package. | S4 |
| 0x8008020F | -2146958833 | APPX_E_INVALID_ DELTA_PACKAGE | Windows app packages (MSIX/AppX) |  | The delta package is invalid. | S4 |
| 0x80080210 | -2146958832 | APPX_E_DELTA_APPENDED_ PACKAGE_NOT_ALLOWED | Windows app packages (MSIX/AppX) |  | The delta appended package is not allowed for the current operation. | S4 |
| 0x80080211 | -2146958831 | APPX_E_INVALID_ PACKAGING_LAYOUT | Windows app packages (MSIX/AppX) |  | The packaging layout file is invalid. | S4 |
| 0x80080212 | -2146958830 | APPX_E_INVALID_ PACKAGESIGNCONFIG | Windows app packages (MSIX/AppX) |  | The packageSignConfig file is invalid. | S4 |
| 0x80080213 | -2146958829 | APPX_E_RESOURCESPRI_ NOT_ALLOWED | Windows app packages (MSIX/AppX) |  | The resources.pri file is not allowed when there are no resource elements in the package manifest. | S4 |
| 0x80080214 | -2146958828 | APPX_E_FILE_ COMPRESSION_MISMATCH | Windows app packages (MSIX/AppX) |  | The compression state of file in baseline and updated package does not match. | S4 |
| 0x80080215 | -2146958827 | APPX_E_INVALID_ PAYLOAD_PACKAGE_EXTENSION | Windows app packages (MSIX/AppX) |  | Non .appx extensions are not allowed for payload packages targeting older platforms. | S4 |
| 0x80080216 | -2146958826 | APPX_E_INVALID_ ENCRYPTION_EXCLUSION_FILE_LIST | Windows app packages (MSIX/AppX) |  | The encryptionExclusionFileList file is invalid. | S4 |
