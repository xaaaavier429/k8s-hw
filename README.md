# k8s-hw

雲端計算與大數據程式設計：K8S 環境安裝與作業一部署（陳維翌）

- `s01`–`s04`：VM 前置、Docker、kubeadm/kubelet/kubectl、cri-dockerd（master 與 work 都跑；work 由 master 複製）
- `w01-rename`：複製出的 work 節點改名
- `m01`–`m04`：master 初始化 control-plane、Flannel、產生 join 指令、檢查節點
- `w02-join`：work 加入叢集
- `h01`–`h04`：作業一（A 數學運算 / B 文字處理 / C 整合平台）建置 image、本機測試、K8S 部署、測試
- `hw1/`：作業一程式碼與 K8S YAML

環境：MacBook Air (Apple Silicon) + VirtualBox，Ubuntu 24.10 arm64，Kubernetes v1.29，cri-dockerd 0.4.7，Flannel。
