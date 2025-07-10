# OCSF-Compliant Wazuh

A project to enhance Wazuh security monitoring with Open Cybersecurity Schema Framework (OCSF) compliance.

## Overview

This project extends Wazuh's capabilities to support OCSF, enabling standardized security data representation and improved interoperability with other security tools.

## Features

- OCSF schema integration for Wazuh alerts
- Standardized security event formatting
- Enhanced data interoperability
- Automated testing framework
- CI/CD pipeline for continuous integration

## Requirements

- Wazuh 4.x or higher
- Python 3.8+
- Docker (for containerized deployment)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/anubhavg-icpl/ocsf-compliant-wazuh.git
cd ocsf-compliant-wazuh
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure Wazuh integration:
```bash
./scripts/setup.sh
```

## Usage

### Basic Configuration

1. Update the configuration file at `config/ocsf-mapping.yml`
2. Deploy the OCSF translator module:
```bash
python src/deploy.py
```

### Running Tests

```bash
pytest tests/
```

## Architecture

The project consists of:
- **Translator Module**: Converts Wazuh alerts to OCSF format
- **Schema Validator**: Ensures OCSF compliance
- **Integration Layer**: Connects with Wazuh API
- **Export Module**: Outputs OCSF-compliant data

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit changes (`git commit -am 'Add new feature'`)
4. Push to branch (`git push origin feature/your-feature`)
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For issues and questions:
- Open an issue on GitHub
- Check the [documentation](docs/)
- Review existing discussions

## Roadmap

- [ ] Full OCSF 1.0 schema support
- [ ] Real-time alert transformation
- [ ] Performance optimization
- [ ] Extended cloud provider support
- [ ] Advanced filtering capabilities

---

**Note**: This project is under active development. Features and APIs may change.
