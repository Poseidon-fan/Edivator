import type { App } from 'vue'
import { Input, Layout, Modal, Select } from 'ant-design-vue'
import VXETable from 'vxe-table'
import Antd from 'ant-design-vue'

export function registerGlobComp(app: App) {
    app.use(Input).use(Layout).use(Modal).use(Select).use(VXETable).use(Antd)
}
