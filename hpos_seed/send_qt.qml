import QtQuick 2.12
import QtQuick.Controls 1.4
import QtQuick.Controls.Styles 1.4
import QtQuick.Dialogs 1.3
import QtQuick.Layouts 1.12

ApplicationWindow {
    property var configFileUrl: null
    property bool success

    visible: true
    title: qsTr("HPOS Seed")

    minimumWidth: 400
    maximumWidth: 400
    minimumHeight: 150
    maximumHeight: 150

    DropArea {
        anchors.fill: parent

        onDropped:
            configFileUrl = drop.text.trim()
    }

    GridLayout {
        id: layout
        focus: true

        Keys.onReturnPressed:
            if (send.enabled) send.clicked()

        anchors.fill: parent
        anchors.margins: 20
 
        columns: 3
        columnSpacing: 10
        rowSpacing: 10

        Label {
            text: qsTr("Config:")
            Layout.alignment: Qt.AlignRight
        }

        // Inspired by GtkFileChooserButton:
        // https://developer.gnome.org/gtk3/stable/GtkFileChooserButton.html
        Button {
            id: configPath 
            iconName: "document-open"
            text: " " + (configFileUrl ? app.file_url_name(configFileUrl): qsTr("Not selected"))

            Layout.columnSpan: 2
            Layout.fillWidth: true

            style: ButtonStyle {
                label: Label {
                    text: configPath.text
                    elide: Text.ElideMiddle
                    verticalAlignment: Text.AlignVCenter
                }
            }
   
            onClicked:
                fileDialog.open()

            FileDialog {
                id: fileDialog

                nameFilters: [
                    qsTr("HPOS config files (hpos-config.json)"),
                    qsTr("All files (*)")
                ]
   
                onAccepted:
                    configFileUrl = fileDialog.fileUrl
            }
        }

        Label {
            text: qsTr("Code:")
            Layout.alignment: Qt.AlignRight
        }
 
        TextField {
            id: wormholeCode

            Layout.columnSpan: 2
            Layout.fillWidth: true
        }

        Label {}

        Label {
            id: status
            text: success ? "✓" : ""

            horizontalAlignment: Text.AlignRight
            Layout.fillWidth: true
        }
 
        Button {
            id: send
            enabled: configFileUrl !== null && app.is_valid_wormhole_code(wormholeCode.text)
            isDefault: true
            text: qsTr("Send")

            onClicked: {
                success = false
                app.send(wormholeCode.text, configFileUrl)
            }
        }
    }

    Connections {
        target: app

        onSuccess:
            success = true
    }

    onClosing:
        app.quit()
}
