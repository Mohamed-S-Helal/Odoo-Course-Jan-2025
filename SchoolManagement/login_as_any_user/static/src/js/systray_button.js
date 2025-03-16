/** @odoo-module **/
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
const { Component } = owl;

/** @extends {Component<UserSwitchWidget>} for switching users */
export class UserSwitchWidget extends Component {
    setup() {
        super.setup();
        this.rpc = useService("rpc");
        this.action = useService("action");
        this.isAdmin = false;
        this.isLoading = true; // Indicate that the admin status is being checked

        // Wait for the admin status check to complete before proceeding
        this._checkAdminGroup().then(() => {
            this.isLoading = false; // No longer loading
            this.render(); // Re-render the component to reflect the updated state
        });
    }

    async _checkAdminGroup() {
        try {
            const result = await this.rpc("/check/admin/group", {});
            this.isAdmin = result.is_admin;
        } catch (error) {
            console.error("Error checking admin group:", error);
        }
    }

    async _onClick() {
        var result = await this.rpc("/switch/user", {});
        if (result == true) {
            this.action.doAction({
                type: 'ir.actions.act_window',
                name: 'Switch User',
                res_model: 'user.selection',
                view_mode: 'form',
                views: [
                    [false, 'form']
                ],
                target: 'new'
            });
        } else {
            this.rpc("/switch/admin", {}).then(function () {
                location.reload();
            });
        }
    }
}

UserSwitchWidget.template = "UserSwitchSystray";

const Systray = {
    Component: UserSwitchWidget
};

registry.category("systray").add("UserSwitchSystray", Systray);
